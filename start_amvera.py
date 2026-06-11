import os
import subprocess
import sys


def run_step(args):
    subprocess.run(args, check=True)


def main():
    os.environ.setdefault('AMVERA', 'true')
    os.environ.setdefault('DEBUG', 'False')
    os.environ.setdefault('DATA_DIR', '/data')

    python = sys.executable
    run_step([python, 'manage.py', 'collectstatic', '--no-input'])
    run_step([python, 'manage.py', 'migrate', '--no-input'])
    run_step([python, 'manage.py', 'load_demo_words'])

    port = os.environ.get('PORT', '80')
    os.execvp(
        'gunicorn',
        [
            'gunicorn',
            'english_vocab_trainer.wsgi:application',
            '--bind',
            f'0.0.0.0:{port}',
        ],
    )


if __name__ == '__main__':
    main()
