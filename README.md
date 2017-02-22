## Python CherryPy ##
The repository provides a ready-to-go setup with following features
* [x] RESTfull
* [x] Unittests
* [x] Simple request test
* [x] Simple HTML template with auto-refresh
* [ ] Authentification user/password
* [ ] Authentification token
* [ ] Authentification token renewal
* [ ] Certifcates usage for HTTPS
* [ ] Deployment with docker
* [ ] Project structure
* [ ] Use root to dispatch many applications (Application and API)

## Install and test ##
```
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python test_mmshop.py
python -m mmshop -h
python -m mmshop [--no-auth]
python demo.py
deactivate
```

## Demo URLS ##
```
http://127.0.0.1:5000/api/v1.0/mmshop/
http://127.0.0.1:5000/api/v1.0/mmshop/item
http://127.0.0.1:5000/api/v1.0/mmshop/item/1
http://127.0.0.1:5000/api/v1.0/mmshop/stats

curl -i -X GET http://127.0.0.1:5000/api/v1.0/mmshop/stats
```

## TODO ##
* unittest should be improved
* in case of error return JSON with error code and message(s)
* add lock for _ITEMS dictionary
* make it true RESTfull - access data attributes by URL
   * example: http://127.0.0.1:5000/api/v1.0/mmshop/item/1/price
* docker deployment
* restructure the project accordingly to
  |__ myproj
  |   |__ __init__.py
  |   |__ config.py
  |   |__ controllers.py
  |   |__ models.py
  |   |__ server.py
  |   |__ static/
  |   |__ lib/
  |   |__ views/
  |       |__ base.tmpl
  |__ README.rd
  |__ requirements.txt
  |__ setup.py
  |__ tests
