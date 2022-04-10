from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36
from django.conf import settings


class TokenGenerator(PasswordResetTokenGenerator):

    def make_token(self, user, email):
        return self._make_token_with_timestamp(user, self._num_seconds(self._now()), email)

    def _make_token_with_timestamp(self, user, timestamp, email):
        ts_b36 = int_to_base36(timestamp)
        hash_string = salted_hmac(
            self.key_salt,
            self._make_hash_value(user, timestamp, email),
            secret=self.secret,
            algorithm=self.algorithm,
        ).hexdigest()[::2]  # Limit to shorten the URL.
        return "%s-%s" % (ts_b36, hash_string)

    def _make_hash_value(self, user, timestamp, email):
        return (
            six.text_type(email) + six.text_type(timestamp)
        )

    def check_token(self, user, token, email):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (email and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts, email), token):
            return False

        # Check the timestamp is within limit.
        if (self._num_seconds(self._now()) - ts) > settings.PASSWORD_RESET_TIMEOUT:
            return False

        return True


account_activation_token = TokenGenerator()
