from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .literals import (
    TEST_CASE_SUPERUSER_EMAIL, TEST_CASE_SUPERUSER_PASSWORD, TEST_CASE_SUPERUSER_USERNAME,
    TEST_CASE_GROUP_NAME, TEST_GROUP_NAME_EDITED, TEST_CASE_USER_EMAIL,
    TEST_CASE_USER_PASSWORD, TEST_CASE_USER_USERNAME, TEST_GROUP_NAME,
    TEST_USER_EMAIL, TEST_USER_USERNAME, TEST_USER_USERNAME_EDITED,
    TEST_USER_PASSWORD
)

__all__ = ('GroupTestMixin', 'UserTestCaseMixin', 'UserTestMixin')


class UserTestCaseMixin(object):
    """
    This TestCaseMixin is used to create an user and group to execute the
    test case, these are used to just create an identity which is required by
    most of the code in the project, these are not meant to be acted upon
    (edited, deleted, etc). To create a test users or groups to modify, use
    the UserTestMixin instead and the respective test_user and test_group.
    The user and group created by this mixin will be prepended with
    _test_case_{...}. The _test_case_user and _test_case_group are meant
    to be used by other test case mixins like the ACLs test case mixin which
    adds shorthand methods to create ACL entries to test access control.
    """
    auto_login_superuser = False
    auto_login_user = True
    create_test_case_superuser = False
    create_test_case_user = True

    def setUp(self):
        super(UserTestCaseMixin, self).setUp()
        if self.create_test_case_user:
            self._create_test_case_user()
            self._create_test_case_group()
            self._test_case_group.user_set.add(self._test_case_user)

            if self.auto_login_user:
                self.login_user()

        if self.create_test_case_superuser:
            self._create_test_case_superuser()

            if self.auto_login_superuser:
                self.login_superuser()

    def tearDown(self):
        self.client.logout()
        super(UserTestCaseMixin, self).tearDown()

    def _create_test_case_group(self):
        self._test_case_group = Group.objects.create(name=TEST_CASE_GROUP_NAME)

    def _create_test_case_superuser(self):
        self._test_case_superuser = get_user_model().objects.create_superuser(
            username=TEST_CASE_SUPERUSER_USERNAME, email=TEST_CASE_SUPERUSER_EMAIL,
            password=TEST_CASE_SUPERUSER_PASSWORD
        )

    def _create_test_case_user(self):
        self._test_case_user = get_user_model().objects.create_user(
            username=TEST_CASE_USER_USERNAME, email=TEST_CASE_USER_EMAIL,
            password=TEST_CASE_USER_PASSWORD
        )

    def login(self, *args, **kwargs):
        logged_in = self.client.login(*args, **kwargs)

        return logged_in

    def login_superuser(self):
        self.login(
            username=TEST_CASE_SUPERUSER_USERNAME,
            password=TEST_CASE_SUPERUSER_PASSWORD
        )

    def login_user(self):
        self.login(
            username=TEST_CASE_USER_USERNAME, password=TEST_CASE_USER_PASSWORD
        )

    def logout(self):
        self.client.logout()


class GroupTestMixin(object):
    def _create_test_group(self):
        self.test_group = Group.objects.create(name=TEST_GROUP_NAME)

    def _edit_test_group(self):
        self.test_group.name = TEST_GROUP_NAME_EDITED
        self.test_group.save()

    def _request_test_group_create_view(self):
        reponse = self.post(
            viewname='user_management:group_create', data={
                'name': TEST_GROUP_NAME
            }
        )
        self.test_group = Group.objects.filter(name=TEST_GROUP_NAME).first()
        return reponse

    def _request_test_group_delete_view(self):
        return self.post(
            viewname='user_management:group_delete', kwargs={
                'group_id': self.test_group.pk
            }
        )

    def _request_test_group_edit_view(self):
        return self.post(
            viewname='user_management:group_edit', kwargs={
                'group_id': self.test_group.pk
            }, data={
                'name': TEST_GROUP_NAME_EDITED
            }
        )

    def _request_test_group_list_view(self):
        return self.get(viewname='user_management:group_list')

    def _request_test_group_members_view(self):
        return self.get(
            viewname='user_management:group_members',
            kwargs={'group_id': self.test_group.pk}
        )


class UserTestMixin(object):
    def _create_test_superuser(self):
        self.test_superuser = get_user_model().objects.create_superuser(
            username=TEST_CASE_SUPERUSER_USERNAME, email=TEST_CASE_SUPERUSER_EMAIL,
            password=TEST_CASE_SUPERUSER_PASSWORD
        )

    def _create_test_user(self):
        self.test_user = get_user_model().objects.create(
            username=TEST_USER_USERNAME, email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD
        )

    def _request_test_superuser_delete_view(self):
        return self.post(
            viewname='user_management:user_delete',
            kwargs={'user_id': self.test_superuser.pk}
        )

    def _request_test_superuser_detail_view(self):
        return self.get(
            viewname='user_management:user_details',
            kwargs={'user_id': self.test_superuser.pk}
        )

    def _request_test_user_create_view(self):
        reponse = self.post(
            viewname='user_management:user_create', data={
                'username': TEST_USER_USERNAME,
                'password': TEST_USER_PASSWORD
            }
        )

        self.test_user = get_user_model().objects.filter(
            username=TEST_USER_USERNAME
        ).first()
        return reponse

    def _request_test_user_delete_view(self):
        return self.post(
            viewname='user_management:user_delete',
            kwargs={'user_id': self.test_user.pk}
        )

    def _request_test_user_edit_view(self):
        return self.post(
            viewname='user_management:user_edit', kwargs={
                'user_id': self.test_user.pk
            }, data={
                'username': TEST_USER_USERNAME_EDITED
            }
        )

    def _request_test_user_groups_view(self):
        return self.get(
            viewname='user_management:user_groups',
            kwargs={'user_id': self.test_user.pk}
        )
