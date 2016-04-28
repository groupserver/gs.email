:mod:`gs.email` Documentation
=============================

This is the core product for *sending* email from GroupServer_
via SMTP [#receiving]_. It is used by the groups to send email to
the group members [#sending]_, and the user-profile system to
send notifications [#notifications]_.

Contents:

.. toctree::
   :maxdepth: 2

   configuration
   troubleshooting
   api
   HISTORY

Resources
=========

- Code repository: https://github.com/groupserver/gs.email/
- Documentation:
  http://groupserver.readthedocs.io/projects/gsemail/
- Questions and comments to
  http://groupserver.org/groups/development/
- Report bugs at https://redmine.iopen.net/projects/groupserver/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

..  LocalWords:  SMTP

.. [#receiving] *Receiving* email is supported by the
   ``gs.group.messages.add.base`` product
   <https://github.com/groupserver/gs.group.messages.add.base>

.. [#sending] *Sending* email from groups is handled by the
              ``gs.group.list.sender`` product
              <https://github.com/groupserver/gs.group.list.sender>

.. [#notifications] Notifications are sent by the
                    ``gs.profile.notify`` product
                    <https://github.com/groupserver/gs.profile.notify/>


.. _GroupServer.org: http://groupserver.org/
.. _GroupServer: http://groupserver.org/
