# Manage System

### file structure 
├──app.py
├──config.py
├──README.md
├──render.py
├──tempCodeRunnerFile.py
│
├─static
│  ├─assets
│  ├─fonts
│  ├─js
│  ├─libs
│  ├─scss
│  └─tasks
│
├─templates
│  │  index.html
│  │
│  ├─horizontal-menu-template
│  │
│  └─vertical-menu-template
│
└─__pycache__
        config.cpython-38.pyc


## app.py
#### change favicon: 
        find:
                <!-- Favicon -->
                <link rel="icon" type="image/x-icon" href="../static/assets/img/favicon/favicon.ico" />
#### change logo: 
        find:
                <span class="app-brand-logo demo">
                ...
                <svg>...</svg>
        replace: 
                <image 
                  src="../static/assets/img/branding/logo.png" 
                  with="40" 
                  heigh="42" 
                  alt="悠悅光">
                <image>
#### change grand name:
        find: <span class="app-brand-text demo menu-text fw-bolder ms-2">Sneat</span>
        replace: <span class="app-brand-text demo menu-text fw-bolder ms-2">悠悅光</span>



## index.html
- PATH: ./templates/index.html
- favicon changed
- logo.png changed

