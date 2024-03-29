import graphene
import graphql_jwt
from django.utils.translation import gettext_lazy as _
from graphene_django_extras import DjangoFilterPaginateListField
from graphql_jwt.decorators import login_required

from user.filters import GrantFilter, UserFilter
from user.mutations import (
    ChangePassword,
    CustomObtainJSONWebToken,
    EmailChange,
    EmailChangeVerify,
    EmailConfirm,
    EmailConfirmVerify,
    GrantMutation,
    PasswordResetChange,
    PhoneNumberChange,
    PhoneNumberChangeVerify,
    PhoneNumberConfirm,
    PhoneNumberConfirmVerify,
    RegisterUser,
    ResetUserPassword,
    ResetUserPasswordVerify,
    SetPassword,
    UpdateUser,
)
from user.types import GrantType, PrivateUserType, UserType


class UserQueries(graphene.ObjectType):
    me = graphene.Field(
        PrivateUserType, description=_("Return the currently authenticated user.")
    )
    grant = DjangoFilterPaginateListField(
        GrantType,
        description="Return the user grant",
        filterset_class=GrantFilter,
    )
    users = DjangoFilterPaginateListField(
        UserType,
        description="Returns user",
        filterset_class=UserFilter,
    )

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        return user if user.is_authenticated else None


class UserMutations(graphene.ObjectType):
    token_auth = CustomObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    change_password = ChangePassword.Field()
    set_password = SetPassword.Field()
    register_user = RegisterUser.Field()
    password_reset = ResetUserPassword.Field()
    password_reset_verify = ResetUserPasswordVerify.Field()
    password_reset_change = PasswordResetChange.Field()
    email_confirm = EmailConfirm.Field()
    email_confirm_verify = EmailConfirmVerify.Field()
    phone_number_confirm = PhoneNumberConfirm.Field()
    phone_number_verify = PhoneNumberConfirmVerify.Field()
    email_change = EmailChange.Field()
    email_change_verify = EmailChangeVerify.Field()
    phone_number_change = PhoneNumberChange.Field()
    phone_number_change_verify = PhoneNumberChangeVerify.Field()
    update_user = UpdateUser.Field()
    create_grant = GrantMutation.Field()
