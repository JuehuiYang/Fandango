# fandango_cli

## Build Setup

```bash
# clone the project
git clone https://github.com/JuehuiYang/Fandango.git

# enter the project directory
cd Fandango/fandango_cli

# install dependency
npm install

# develop
npm run dev
```

This will automatically open http://localhost:9528

## Build

```bash
# build for test environment
npm run build:stage

# build for production environment
npm run build:prod
```

## Advanced

```bash
# preview the release environment effect
npm run preview

# preview the release environment effect + static resource analysis
npm run preview -- --report

# code format check
npm run lint

# code format check and auto fix
npm run lint -- --fix
```

## License

The project is based on [vue-admin-template](https://github.com/PanJiaChen/vue-admin-template)

[MIT](https://github.com/PanJiaChen/vue-admin-template/blob/master/LICENSE) license.

Copyright (c) 2017-present PanJiaChen
