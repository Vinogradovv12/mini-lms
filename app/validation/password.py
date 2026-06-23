import re


class PasswordValidator:

    @staticmethod
    def validate(
        password: str
    ) -> str:

        if len(password) < 8:
            raise ValueError(
                "Password must contain at least 8 characters"
            )

        if not re.search(
            r"[A-Z]",
            password
        ):
            raise ValueError(
                "Password must contain uppercase letter"
            )

        if not re.search(
            r"[a-z]",
            password
        ):
            raise ValueError(
                "Password must contain lowercase letter"
            )

        if not re.search(
            r"\d",
            password
        ):
            raise ValueError(
                "Password must contain number"
            )

        return password