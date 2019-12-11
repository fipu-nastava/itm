import argparse
from application.view import create_app
from application.task_ai import train, predict

parser = argparse.ArgumentParser()
parser.add_argument("--train", action='store_true', help="Train model")
parser.add_argument("--test", action='store_true', help="Test model")
parser.add_argument("--predict", help="Predict with input")

app = create_app()

if __name__ == "__main__":

    """
        CMD naredbe:
        - python task_ai.py --train
        - python task_ai.py --test
        - python task_ai.py --predict "Give access to trello, email"
    """

    args = parser.parse_args()

    if args.train:
        train()

    elif args.test:
        print(predict("email daniel about"))
        print(predict("Confirm final details with phot"))
        print(predict("Schedule appointments with site ma"))

    elif args.predict:
        print(predict(args.predict))

    else:
        app.run(debug=True, port=8011)
