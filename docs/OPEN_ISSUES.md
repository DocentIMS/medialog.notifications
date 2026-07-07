# Open Issues / Follow-ups

Tracked here because this repository is a fork without an Issues tab.

Last reviewed: 2026-07-07

## Fixed (branch `claude/code-review-security-crashes-ls8wso`)

- `views/remove_notification.py` — bad/missing `?item=` UID crashed with a 500;
  redirected to the raw `Referer` (open redirect). Guarded + same-origin redirect.
- `api/services/remove_notification/patch.py` — write logic assigned `None` and
  passed a member object instead of a user id; never worked. Rewritten; `print`
  replaced with `logger.exception`.
- `subscribers/mention_user_from_text.py` — `None`/non-str comment text raised
  `TypeError`; `notify_users` was wrapped in a tuple containing a list. Fixed.
- `views/email_notification_view.py` — crashed on a notification with no message
  body and sent spurious "0 notifications" emails. Guarded.
- `subscribers/notification_handler.py` — use `user.getId()` for consistency.
- `subscribers/mention_user_from_text.py` — `MENTION_RE` no longer matches the
  domain part of email addresses (`foo@bar.com`). The `@` must now be at the
  start of the text or preceded by whitespace, and only valid username
  characters (no trailing punctuation) are captured.
- `api/services/mentions_view/get.py` — the user directory (fullname + username)
  is now only returned to authenticated members; anonymous requests raise
  `Unauthorized`. Policy decision: every member may see other members' names.
- `views/configure.zcml` — `email-notification-view` permission changed from
  `zope2.View` to `cmf.ManagePortal`, so only a Manager (a scheduler/admin
  action running with sufficient rights) can trigger the all-users email batch.

## Still open

_None — all items from the review have been addressed._

Note on `email-notification-view`: there is no trigger for it anywhere in the
code (no cron/clock registration). Whatever fires it (an admin action or an
external scheduler) must now run with Manager rights. If a normal-user action
should ever kick off the digest, wire that action to run the batch server-side
rather than exposing this URL to non-managers.
