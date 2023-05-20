// index.js

const gulp = require('gulp');
const sass = require('gulp-sass');
const autoprefixer = require('gulp-autoprefixer');
const uglify = require('gulp-uglify');

// Define your Gulp tasks for Django integration
gulp.task('build:static', function () {
  // Task for compiling Sass
  gulp.src('path/to/sass/files/**/*.scss')
    .pipe(sass())
    .pipe(autoprefixer())
    .pipe(gulp.dest('path/to/static/css'));

  // Task for minifying JavaScript
  gulp.src('path/to/js/files/**/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('path/to/static/js'));

  // Additional tasks for other static files (images, fonts, etc.)
  // ...

  // You can also include a task to copy static files to Django's static directory
  gulp.src('path/to/static/**/*')
    .pipe(gulp.dest('path/to/django/static'));
});

// Define a default task that runs all the required tasks
gulp.task('default', gulp.series('build:static'));
