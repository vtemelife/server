from .generic import BaseEmail


class SignUpVerification(BaseEmail):
    body = "users/sign_up_verification_body.html"
    subject = "users/sign_up_verification_subject.html"


class ResetPasswordVerification(BaseEmail):
    body = "users/reset_password_verification_body.html"
    subject = "users/reset_password_verification_subject.html"
