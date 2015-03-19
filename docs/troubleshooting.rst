Troubleshooting
===============

If mail is trapped in ``queuedir/new`` look to see if
``.sending_*`` or ``.rejected_*`` files have been created in the
same directory. If so, delete them and the mail should be
processed.
