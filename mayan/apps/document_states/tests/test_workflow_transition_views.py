from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.events.tests.mixins import EventTestCaseMixin
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_workflow_edited
from ..literals import WIDGET_CLASS_TEXTAREA
from ..models import WorkflowTransition
from ..permissions import (
    permission_workflow_edit, permission_workflow_transition,
    permission_workflow_view
)

from .literals import (
    TEST_WORKFLOW_TRANSITION_LABEL, TEST_WORKFLOW_TRANSITION_LABEL_EDITED
)
from .mixins import (
    WorkflowTestMixin, WorkflowTransitionEventViewTestMixin,
    WorkflowTransitionFieldTestMixin, WorkflowTransitionFieldViewTestMixin,
    WorkflowViewTestMixin, WorkflowTransitionViewTestMixin
)


class WorkflowTransitionViewTestCase(
    EventTestCaseMixin, WorkflowTestMixin, WorkflowViewTestMixin,
    WorkflowTransitionViewTestMixin, GenericViewTestCase
):
    _test_event_object_name = 'test_workflow'

    def test_workflow_transition_create_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._clear_events()

        response = self._request_test_workflow_transition_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(WorkflowTransition.objects.count(), 0)
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_transition_create_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._clear_events()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_transition_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WorkflowTransition.objects.count(), 1)
        self.assertEqual(
            WorkflowTransition.objects.all()[0].label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )
        self.assertEqual(
            WorkflowTransition.objects.all()[0].origin_state,
            self.test_workflow_state_1
        )
        self.assertEqual(
            WorkflowTransition.objects.all()[0].destination_state,
            self.test_workflow_state_2
        )
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_transition_delete_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._clear_events()

        response = self._request_test_workflow_transition_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_transition in WorkflowTransition.objects.all()
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_transition_delete_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._clear_events()

        self.grant_access(permission=permission_workflow_edit, obj=self.test_workflow)

        response = self._request_test_workflow_transition_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            self.test_workflow_transition in WorkflowTransition.objects.all()
        )
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_transition_edit_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._clear_events()

        response = self._request_test_workflow_transition_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_transition.label, TEST_WORKFLOW_TRANSITION_LABEL
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_transition_edit_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._clear_events()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_transition_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL_EDITED
        )
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_transition_list_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._clear_events()

        response = self._request_test_workflow_transition_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow_transition.label,
            status_code=404
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_transition_list_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._clear_events()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_transition_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_transition.label,
            status_code=200
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)


class WorkflowTransitionDocumentViewTestCase(
    WorkflowTestMixin, WorkflowViewTestMixin, WorkflowTransitionViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow()
        self.test_workflow.document_types.add(self.test_document_type)
        self._create_test_workflow_states()
        self._create_test_workflow_transitions()
        self._upload_test_document()
        self.test_workflow_instance = self.test_document.workflows.first()

    def test_workflow_transition_selection_get_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )
        response = self._request_test_workflow_transition_selection_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

    def test_workflow_transition_selection_post_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )
        response = self._request_test_workflow_transition_selection_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

    def test_workflow_transition_execute_view_no_permission(self):
        """
        Test transitioning a workflow without the transition workflow
        permission.
        """
        response = self._request_test_workflow_transition_execute_view()
        self.assertEqual(response.status_code, 404)

        # Workflow should remain in the same initial state
        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

    def test_workflow_transition_execute_view_with_workflow_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )

        response = self._request_test_workflow_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )

    def test_workflow_transition_execute_view_with_transition_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self.grant_access(
            obj=self.test_workflow_transition,
            permission=permission_workflow_transition
        )

        response = self._request_test_workflow_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )


class WorkflowTransitionEventViewTestCase(
    WorkflowTestMixin, WorkflowTransitionEventViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_workflow_transition_event_list_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        response = self._request_test_workflow_transition_event_list_view()
        self.assertEqual(response.status_code, 404)

    def test_workflow_transition_event_list_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_transition_event_list_view()
        self.assertEqual(response.status_code, 200)


class WorkflowTransitionFieldViewTestCase(
    EventTestCaseMixin, WorkflowTestMixin, WorkflowTransitionFieldTestMixin,
    WorkflowTransitionFieldViewTestMixin, WorkflowTransitionViewTestMixin,
    GenericViewTestCase
):
    _test_event_object_name = 'test_workflow'

    def setUp(self):
        super().setUp()
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

    def test_workflow_transition_field_create_view_no_permission(self):
        workflow_transition_field_count = self.test_workflow_transition.fields.count()
        self._clear_events()

        response = self._request_workflow_transition_field_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_transition_field_create_view_with_access(self):
        workflow_transition_field_count = self.test_workflow_transition.fields.count()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        self._clear_events()

        response = self._request_workflow_transition_field_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count + 1
        )
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_transition_field_delete_view_no_permission(self):
        self._create_test_workflow_transition_field()
        workflow_transition_field_count = self.test_workflow_transition.fields.count()
        self._clear_events()

        response = self._request_workflow_transition_field_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_transition_field_delete_view_with_access(self):
        self._create_test_workflow_transition_field()
        workflow_transition_field_count = self.test_workflow_transition.fields.count()
        self._clear_events()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_workflow_transition_field_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count - 1
        )
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_transition_field_edit_view_no_permission(self):
        self._create_test_workflow_transition_field()
        workflow_transition_field_label = self.test_workflow_transition_field.label
        self._clear_events()

        response = self._request_workflow_transition_field_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_transition_field.refresh_from_db()
        self.assertEqual(
            workflow_transition_field_label,
            self.test_workflow_transition_field.label
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_transition_field_edit_view_with_access(self):
        self._create_test_workflow_transition_field()
        workflow_transition_field_label = self.test_workflow_transition_field.label
        self._clear_events()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_workflow_transition_field_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_transition_field.refresh_from_db()
        self.assertNotEqual(
            workflow_transition_field_label,
            self.test_workflow_transition_field.label
        )
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_transition_field_list_view_no_permission(self):
        self._create_test_workflow_transition_field()
        self._clear_events()

        response = self._request_test_workflow_transition_field_list_view()
        self.assertNotContains(
            response=response,
            text=self.test_workflow_transition_field.label,
            status_code=404
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_transition_field_list_view_with_access(self):
        self._create_test_workflow_transition_field()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        self._clear_events()

        response = self._request_test_workflow_transition_field_list_view()
        self.assertContains(
            response=response,
            text=self.test_workflow_transition_field.label,
            status_code=200
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)


class WorkflowInstanceTransitionFieldViewTestCase(
    WorkflowTestMixin, WorkflowTransitionFieldTestMixin,
    WorkflowTransitionFieldViewTestMixin, WorkflowTransitionViewTestMixin,
    GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._create_test_workflow_transition_field(
            extra_data={
                'widget': WIDGET_CLASS_TEXTAREA
            }
        )
        self._upload_test_document()
        self.test_workflow_instance = self.test_document.workflows.first()

    def test_workflow_transition_text_area_widget_execute_view_with_transition_access(self):
        self.grant_access(
            obj=self.test_workflow_transition,
            permission=permission_workflow_transition
        )

        response = self._request_test_workflow_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )
