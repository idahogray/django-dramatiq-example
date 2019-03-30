from django.core import mail
from django.db import connections
from django.test import TestCase

from django_dramatiq.test import DramatiqTestCase

from .models import AModel
from .tasks import send_email_1
from .tasks import send_email_2
from .tasks import send_email_3
from .tasks import send_email_4
from .tasks import send_email_5


def close_db_connections(func, *args, **kwargs):
    """
    Decorator to explicitly close db connections during threaded execution

    Note this is necessary to work around:
    https://code.djangoproject.com/ticket/22420
    """
    def _close_db_connections(*args, **kwargs):
        print("Closing Connections")
        ret = None
        try:
            ret = func(*args, **kwargs)
        finally:
            for conn in connections.all():
                conn.close()
        return ret
    return _close_db_connections


class DramatiqTestCaseCloseConnTeardown(DramatiqTestCase):
    """This class is used to over-ride the teardown for the worker created in 
    DramatiqTestCase. It adds close_db_connections as a decorator per
    the ticket listed in the decorator description.
    """
    @close_db_connections
    def _post_teardown(self):
        print("Stopping Worker")
        self.worker.stop()

        super()._post_teardown()


class DramatiqTaskTest(DramatiqTestCaseCloseConnTeardown):
    def test_send_email_task(self):
        send_email_1.send('This is a test subject')
        send_email_2.send('This is a test subject')
        send_email_3.send('This is a test subject')
        send_email_4.send('This is a test subject')
        send_email_5.send('This is a test subject')
        for queue in self.broker.get_declared_queues():
            self.broker.join(queue)
        self.worker.join()
        self.assertEqual(len(mail.outbox), 5)
        self.assertIn('idahogray@gmail.com', mail.outbox[0].to)
        self.assertEqual(mail.outbox[0].from_email, 'idahogray@gmail.com')
        self.assertEqual(mail.outbox[0].subject, 'This is a test subject')
        self.assertEqual(mail.outbox[0].body, 'This is a test body')

    def test_send_email_view(self):
        self.client.get('/dramatiq/send_email/')
        for queue in self.broker.get_declared_queues():
            self.broker.join(queue)
        self.worker.join()
        self.assertEqual(len(mail.outbox), 5)
        self.assertIn('idahogray@gmail.com', mail.outbox[0].to)
        self.assertEqual(mail.outbox[0].from_email, 'idahogray@gmail.com')
        self.assertEqual(mail.outbox[0].subject, 'View Subject')
        self.assertEqual(mail.outbox[0].body, 'This is a test body')

    def test_send_email_view_with_db(self):
        a_model = AModel.objects.create(a_field='Test Field')
        self.client.get('/dramatiq/send_email/')
        for queue in self.broker.get_declared_queues():
            self.broker.join(queue)
        self.worker.join()
        self.assertEqual(len(mail.outbox), 5)
