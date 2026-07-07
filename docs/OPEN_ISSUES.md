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

## Still open (need a product decision — not yet changed)

### 1. `@mentions_view` leaks the full user directory
`api/services/mentions_view/get.py` + its `configure.zcml`

The service is registered with `permission="zope2.View"` and returns every
user's fullname and username. Any user who can View the site can enumerate all
accounts. Decision needed: restrict to an authenticated/manager permission, or
accept the exposure.

### 2. `email-notification-view` can be triggered by any viewer
`views/email_notification_view.py` + `views/configure.zcml`

Registered `for=IPloneSiteRoot` with `permission="zope2.View"`. Any viewer can
hit `/@@email-notification-view`, which loops all users and sends each their
notifications — an abuse / DoS / mail-flooding vector. It is presumably meant to
run from a clock/cron. Decision needed: restrict to `cmf.ManagePortal` (or a
dedicated permission), confirming the scheduler runs with sufficient rights.

_(Item 3, the mention regex matching email domains, has been fixed — see the
"Fixed" section above.)_
