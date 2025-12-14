import unittest

from email_service import valida_email_indirizzi, _normalizza_lista_email


class TestEmailValidation(unittest.TestCase):
    def test_valid_addresses(self):
        valido, msg = valida_email_indirizzi(
            "sender@example.com",
            "dest@example.com",
            "cc1@example.com, cc2@example.org",
            "bcc@example.net",
        )
        self.assertTrue(valido)
        self.assertEqual(msg, "")

    def test_invalid_sender(self):
        valido, msg = valida_email_indirizzi(
            "invalid", "dest@example.com", "", ""
        )
        self.assertFalse(valido)
        self.assertIn("Mittente", msg)

    def test_invalid_list(self):
        valido, msg = valida_email_indirizzi(
            "sender@example.com", "dest@example.com", "good@example.com, bad", ""
        )
        self.assertFalse(valido)
        self.assertIn("CC", msg)

    def test_normalizza_lista_email(self):
        emails = _normalizza_lista_email(" a@example.com , , b@example.com ")
        self.assertEqual(emails, ["a@example.com", "b@example.com"])


if __name__ == "__main__":
    unittest.main()
