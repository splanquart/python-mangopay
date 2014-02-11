.. _ref-signals:

=======
Signals
=======

To debug some feature we want to know what data are send to MangoPay.
For do that you can use signals pluged in python-mangopay.

There is 5 signals :

 - request_finished
 - request_started
 - request_error
 - pre_save
 - post_save

Example ::

    from mangopay.signals import request_started

    def print_infos(signal, **kw):
        print("Before send data : %r" % kw)

    request_started.connect(print_infos)

    # do something with python-mangopay

