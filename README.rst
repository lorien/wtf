WTF - linux system state overview with one command
==================================================

WTF is the command get idea WTF is going on in your linux system. It displays info that
makes sense to me on my servers. Probably it would be useful to you too.


Installation
------------

.. code:: bash

    pip install -U pywtf


User Manual
-----------

Say WTF and then run the command

.. code:: bash

    $ ./wtf 
    (HOST) aragorn
    (PROC) 387 | bash 20 | chrome 13 | x-terminal-emul 8 | ssh 6 | postgres 6
    (LOAD) 0.21 | 0.15 | 0.14
    (MEM) total 7.7G | used 2.1G | avail 5.6G
    (TCP) inuse 22 | orphan 0 | tw 0 | alloc 33


Feedback
--------

Drop a mail to lorien@lorien.name or create github issue.
