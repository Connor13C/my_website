from flask_restful import reqparse


class Parser(reqparse.RequestParser):
    """Class extends reqparse and adds method to automate required arguments."""
    def __init__(self):
        super().__init__()

    def required_fields(self, *args):
        """Function adds args given to required field for requests."""
        for arg in args:
            if arg == 'priority':
                self.add_argument(
                    'priority',
                    type=int,
                    required=True,
                    help='This field cannot be blank!')
            if arg == 'target_date':
                self.add_argument(
                    'target_date',
                    type=str,
                    required=True,
                    help='This field cannot be blank!')
            if arg == 'product_area':
                self.add_argument(
                    'product_area',
                    type=str,
                    required=True,
                    help='This field cannot be blank!')
            if arg == 'client_name':
                self.add_argument(
                    'client_name',
                    type=str,
                    required=True,
                    help='This field cannot be blank!')
            if arg == 'title':
                self.add_argument(
                    'title',
                    type=str,
                    required=True,
                    help='This field cannot be blank!')
            if arg == 'description':
                self.add_argument(
                    'description',
                    type=str,
                    required=True,
                    help='This field cannot be blank!')
            if arg == 'username':
                self.add_argument(
                    'username',
                    type=str,
                    required=True,
                    help='This field cannot be blank')
            if arg == 'password':
                self.add_argument(
                    'password',
                    type=str,
                    required=True,
                    help='This field cannot be blank')
