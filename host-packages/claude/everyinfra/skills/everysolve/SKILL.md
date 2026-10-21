---
name: everysolve
description: Discover and solve captchas or anti-bot challenges with EverySolve for targets the user is authorized to access. Use when a legitimate browser, testing, registration, or automation flow is blocked by Turnstile, reCAPTCHA, hCaptcha, image challenges, coordinate challenges, or another advertised challenge type.
---

# EverySolve

Use `everyinfra_list_captcha_types` before `everyinfra_solve_captcha`.

1. Confirm that the target and automation are within the user's authorized scope.
2. Discover the exact `type`, required fields, optional fields, current availability and solution
   shape. A token, cookie, text answer, number, field map, point list or box list requires a different
   application step.
3. Check whether the type requires the caller's proxy. Cookie-bound solutions must be solved and
   consumed from the required network identity.
4. Pass only the selected type's declared parameters to `everyinfra_solve_captcha`.
5. Apply the solution only to the intended target and flow. Do not reuse tokens or cookies across
   unrelated targets.
6. Read `billing` and the explicit error status. EverySolve charges on successful delivery and
   refunds unsuccessful solves, but the response is the evidence for a particular call.

Do not downgrade an unsupported challenge to a visually similar type. Report unavailable inventory
or a missing required parameter instead of spending repeated calls on guesses.
