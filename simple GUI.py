from gooey import Gooey, GooeyParser

@Gooey( advanced = True,
        required_cols = 1,
        show_sidebar = True,
        program_name = "DataP",
        program_description = "a data quality tool developed based on Deequ to perform anomaly detection.",
        
        menu=[{'name': 'File', 'items': []},
              {'name': 'Tools', 'items': []},
              {'name': 'Help', 'items': []}])

def main():
  parser = GooeyParser()
  subs = parser.add_subparsers(help='commands', dest='command')

  subparser1 = subs.add_parser('Load Analyzer')
  apply_my_common_args1(subparser1)

  subparser2 = subs.add_parser('Load Check')
  apply_my_common_args2(subparser2)

  args = parser.parse_args()

def apply_my_common_args1(subparser):
    subparser.add_argument('dataset', help="name of dataset to process", widget='FileChooser')
    subparser.add_argument('analyzer.py', help="analyzer.py file to perform basic analysis", widget='FileChooser')

def apply_my_common_args2(subparser):
    subparser.add_argument('dataset', help="name of dataset to process", widget='FileChooser')
    subparser.add_argument('check.py', help="check.py file to perform anomaly detection", widget='FileChooser')
    subparser.add_argument(
        '--load',
        metavar='Load Suggestion',
        help='Load constraint suggestions',
        dest='filename',
        widget='CheckBox',
    )

if __name__ == "__main__":
    main()