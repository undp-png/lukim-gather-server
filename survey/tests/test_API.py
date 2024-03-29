import io
import json
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.gis import geos
from django.utils import timezone
from graphql_jwt.shortcuts import get_token
from PIL import Image

from lukimgather.tests import TestBase


class APITest(TestBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        users = cls.baker.make(
            settings.AUTH_USER_MODEL, is_active=True, is_staff=True, _quantity=1
        )
        cls.activated_initial_password = get_user_model().objects.make_random_password()
        users[0].set_password(cls.activated_initial_password)
        users[0].save()
        cls.category = cls.baker.make(
            "survey.ProtectedAreaCategory", title="test", _quantity=1
        )[0]
        cls.project = cls.baker.make(
            "project.Project", title="project test", _quantity=1
        )[0]
        cls.happening_survey = cls.baker.make(
            "survey.HappeningSurvey", title="test", _quantity=1
        )[0]
        cls.activated_user = authenticate(
            username=users[0].username, password=cls.activated_initial_password
        )
        cls.headers = {"HTTP_AUTHORIZATION": f"Bearer {get_token(users[0])}"}

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)
        return file

    def test_survey_get(self):
        response = self.query(
            """
            query {
              happeningSurveys {
                id
              }
            }
            """,
            headers=self.headers,
        )
        self.assertResponseNoErrors(response)

    def test_categories_get(self):
        response = self.query(
            """
            query {
              protectedAreaCategories {
                id
                title
                child {
                  id
                  title
                }
              }
            }
            """,
            headers=self.headers,
        )
        self.assertResponseNoErrors(response)

    def test_create_happening_survey(self):
        mutation = """
            mutation CreateHappeningSurvey($data: HappeningSurveyInput!) {
                createHappeningSurvey(data: $data) {
                    ok
                    result
                        {
                            id
                        }
                    errors
                }
            }
        """
        data_with_id = {
            "id": str(uuid4()),
            "title": "test title",
            "description": "test description",
            "sentiment": "\U0001f600",
            "improvement": "INCREASING",
            "location": str(geos.Point(1, 0)),
            "projectId": self.project.id,
            "categoryId": self.category.id,
            "isPublic": False,
            "isTest": True,
            "attachment": [None, None],
            "createdAt": timezone.now().isoformat(),
        }
        data_without_id = {
            "title": "test title",
            "description": "test description",
            "sentiment": "\U0001f600",
            "improvement": "INCREASING",
            "location": str(geos.Point(1, 0)),
            "projectId": self.project.id,
            "categoryId": self.category.id,
            "isPublic": False,
            "isTest": True,
            "attachment": [None, None],
            "createdAt": timezone.now().isoformat(),
        }
        response_with_id = self.client.post(
            self.GRAPHQL_URL,
            data={
                "operations": json.dumps(
                    {
                        "query": mutation,
                        "variables": {
                            "data": data_with_id,
                        },
                    }
                ),
                "0": self.generate_photo_file(),
                "1": self.generate_photo_file(),
                "map": json.dumps(
                    {
                        "0": ["variables.data.attachment.0"],
                        "1": ["variables.data.attachment.1"],
                    }
                ),
            },
            **self.headers,
        )
        response_without_id = self.client.post(
            self.GRAPHQL_URL,
            data={
                "operations": json.dumps(
                    {
                        "query": mutation,
                        "variables": {
                            "data": data_without_id,
                        },
                    }
                ),
                "0": self.generate_photo_file(),
                "1": self.generate_photo_file(),
                "map": json.dumps(
                    {
                        "0": ["variables.data.attachment.0"],
                        "1": ["variables.data.attachment.1"],
                    }
                ),
            },
            **self.headers,
        )
        self.assertResponseNoErrors(response_with_id)
        self.assertResponseNoErrors(response_without_id)

    def test_survey_form_get(self):
        response = self.query(
            """
            query {
              surveyForm {
                id
                code
                title
                xform
              }
            }
            """,
            headers=self.headers,
        )
        self.assertResponseNoErrors(response)

    def test_update_happening_survey(self):
        mutation = """
            mutation UpdateHappeningSurvey($data: UpdateHappeningSurveyInput!, $id: UUID!) {
                  updateHappeningSurvey(data: $data, id: $id) {
                    ok
                    result {
                        id
                        title
                        description
                        sentiment
                        improvement
                        location {
                          type
                          coordinates
                        }
                        category {
                          id
                        }
                        attachment {
                          id
                        }
                    }
                    errors
                  }
            }
        """
        data = {
            "title": "test title",
            "description": "test description",
            "sentiment": "\U0001f600",
            "improvement": "INCREASING",
            "location": str(geos.Point(1, 0)),
            "categoryId": self.category.id,
            "attachment": [None],
            "modifiedAt": timezone.now().isoformat(),
        }
        response = self.client.post(
            self.GRAPHQL_URL,
            data={
                "operations": json.dumps(
                    {
                        "query": mutation,
                        "variables": {
                            "data": data,
                            "id": str(self.happening_survey.id),
                        },
                    }
                ),
                "0": self.generate_photo_file(),
                "map": json.dumps(
                    {
                        "0": ["variables.data.attachment.0"],
                    }
                ),
            },
            **self.headers,
        )
        self.assertResponseNoErrors(response)

    def test_edit_happening_survey(self):
        mutation = """
            mutation EditHappeningSurvey($data: UpdateHappeningSurveyInput!, $id: UUID!) {
                  editHappeningSurvey(data: $data, id: $id) {
                    ok
                    result {
                        id
                        title
                        description
                        sentiment
                        improvement
                        location {
                          type
                          coordinates
                        }
                        category {
                          id
                        }
                        attachment {
                          id
                        }
                    }
                    errors
                  }
            }
        """
        data = {
            "title": "test title",
            "description": "test description",
            "sentiment": "\U0001f600",
            "improvement": "INCREASING",
            "location": str(geos.Point(1, 0)),
            "categoryId": self.category.id,
            "attachment": [None],
        }
        response = self.client.post(
            self.GRAPHQL_URL,
            data={
                "operations": json.dumps(
                    {
                        "query": mutation,
                        "variables": {
                            "data": data,
                            "id": str(self.happening_survey.id),
                        },
                    }
                ),
                "0": self.generate_photo_file(),
                "map": json.dumps(
                    {
                        "0": ["variables.data.attachment.0"],
                    }
                ),
            },
            **self.headers,
        )
        self.assertResponseNoErrors(response)

    def test_happening_survey_history_get(self):
        response = self.query(
            """
            query {
              happeningSurveysHistory {
                id
                objectRepr
                objectId
                format
                db
                revision {
                  id
                  comment
                  dateCreated
                }
                serializedData {
                  fields {
                    title
                    description
                    improvement
                    sentiment
                    status
                    isPublic
                    isTest
                    region {
                      id
                      name
                    }
                    location {
                      type
                      coordinates
                    }
                    boundary {
                      type
                      coordinates
                    }
                    protectedArea {
                      id
                      name
                    }
                    project {
                      id
                    }
                    category {
                      id
                      title
                    }
                    createdBy {
                      id
                      firstName
                      lastName
                    }
                    updatedBy {
                      id
                      firstName
                      lastName
                    }
                    createdAt
                    modifiedAt
                  }
                }
              }
            }
            """,
            headers=self.headers,
        )
        self.assertResponseNoErrors(response)
