# Recreational-Club-Membership

Task Description:

The context of this project is a small amateur club (think salsa dancing or something like that) with a couple of dozen members. 
The club meets once a week for practice, and they are coached by an amateur coach. 
Members are free to show up (or not) every time. When they show up, they should pay for each practice, say, $10, but they may also pay for up to one month in advance; some discount may be given if so desired. 
Once a month, the treasurer pays the rent for the hall in which the club meets, and the coach should be paid monthly or biweekly, but only for the practices that she has attended (she has a full-time job which sometimes requires her to be unavailable for the practice). 
The app should keep track of finances for the club and for each member, as they sometimes show up for practice but manage to sneak out without paying. 
It may also send reminders to members about forthcoming practices, both regular and ad hoc ones, and threaten those who are a bit too casual with their payments

## Run Locally

Clone the project

```bash
  git clone https://github.com/Raymond3lam/Recreational-Club-Membership.git
```

Go to the project directory

```bash
  cd Recreational-Club-Membership 
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Apply Database Migrations

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```

View application at

```bash
  http://127.0.0.1:8000/
```

## Contributing

Parsa, Chris, Raymond, Luxman, Irfan

## Tech Stack

- Django (python)
- Database: SQL

