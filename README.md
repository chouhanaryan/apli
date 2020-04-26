<h1 align="center">Moo: Movie Website</h1>
<h4 align='center'>A movie viewing website with like/dislike, comments and admin/user functionality</h4>

## Demo

### Live demo

The website is live at [https://moviesdjango.pythonanywhere.com/](https://moviesdjango.pythonanywhere.com/).

### Video demo (outdated)

[![Alt text](https://img.youtube.com/vi/8R-Uch6WbaQ/0.jpg)](https://www.youtube.com/watch?v=8R-Uch6WbaQ)

## Build Instructions

```bash
git clone https://github.com/chouhanaryan/moo.git
cd .\moo\
pip3 install -r requirements.txt
cd .\moo\
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
#### Superuser creation

After migrations, run the ```createsuperuser``` command and enter the required details

```bash
python3 manage.py createsuperuser
```
