def activation_mail_html(user, activation_link):
    """
    The function `activation_mail_html` generates an HTML email template for sending activation links to
    users.
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Activate your Videoflix account</title>
    </head>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color:#ffffff;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td align="center" style="padding:40px 0;">
                    <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;">
                        <tr>
                            <td style="color:#333333; font-size:16px; line-height:1.5;">
                                <p>Dear {user.email},</p>
                                <p>
                                    Thank you for registering with <strong>Videoflix</strong>.  
                                    To complete your registration and verify your email address, please click the link below:
                                </p>
                            </td>
                        </tr>
                        <tr>
                            <td align="center" style="padding:30px 0;">
                                <a href="{activation_link}"
                                   style="
                                   background-color:#4F46E5;
                                   color:#ffffff;
                                   text-decoration:none;
                                   padding:14px 28px;
                                   border-radius:30px;
                                   font-weight:bold;
                                   display:inline-block;
                                   ">
                                    Activate account
                                </a>
                            </td>
                        </tr>
                        <tr>
                            <td style="color:#666666; font-size:14px; line-height:1.5;">
                                <p>
                                    If you did not create an account with us, please disregard this email.
                                </p>
                                <p>
                                    Best regards,<br>
                                    Your Videoflix Team.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

def activation_mail_text(user, activation_link):
    """
    The function `activation_mail_text` generates an activation email message with a personalized
    greeting and activation link for a user.
    """
    return f"""
    Hi {user.email},

    Thank you for registering with Videoflix.
    Please activate your account using the following link:

    {activation_link}

    If you did not create an account, please ignore this email.

    Best regards,
    Your Videoflix Team
    """


def reset_mail_html(reset_link):
    """
    The function `reset_mail_html` generates an HTML email template for resetting a user's password,
    including the user's email and a reset link.
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Reset your Password</title>
    </head>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color:#ffffff;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td align="center" style="padding:40px 0;">
                    <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;">
                        <tr>
                            <td style="color:#333333; font-size:16px; line-height:1.5;">
                                <p>Hello,</p>
                                <p>
                                    We recently received a request to reset your password. If you made this request, please click on the following link to reset your password:
                                </p>
                            </td>
                        </tr>
                        <tr>
                            <td align="center" style="padding:30px 0;">
                                <a href="{reset_link}"
                                   style="
                                   background-color:#4F46E5;
                                   color:#ffffff;
                                   text-decoration:none;
                                   padding:14px 28px;
                                   border-radius:30px;
                                   font-weight:bold;
                                   display:inline-block;
                                   ">
                                    Reset password
                                </a>
                            </td>
                        </tr>
                        <tr>
                            <td style="color:#666666; font-size:14px; line-height:1.5;">
                                <p>
                                    Please note that for security reasons, this link is only valid for 24 hours.
                                </p>
                                <p>
                                    If you did not request a password reset, please ignore this email.
                                </p>
                                <p>
                                    Best regards,<br>
                                    Your Videoflix Team.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def reset_mail_text(user, reset_link):
    """
    The function `reset_mail_text` generates a password reset email message with the user's email and a
    reset link.
    """
    return f"""
    Hello,

    We recently received a request to reset your password. 
    If you made this request, please click on the following link to reset your password:

    {reset_link}

    Please note that for security reasons, this link is only valid for 24 hours.
    If you did not request a password reset, please ignore this email.

    Best regards,
    Your Videoflix Team
    """