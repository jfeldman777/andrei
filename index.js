// index.js

 const gulp = require('gulp');
 const sass = require('gulp-sass');
 const autoprefixer = require('gulp-autoprefixer');
const uglify = require('gulp-uglify');


const autoprefixer = require("gulp-autoprefixer");
const browserSync = require("browser-sync").create();
const cleanCss = require("gulp-clean-css");
const del = require("del");
const fs = require("fs");
const gulp = require("gulp");
const path = require("path");
const rename = require("gulp-rename");
//const sass = require("gulp-sass")(require("sass"));
const sourcemaps = require("gulp-sourcemaps");
const spawn = require("child_process").spawn;
const wait = require("gulp-wait");
const { groupCollapsed } = require("console");

const paths = {
  src: {
    root: "./",
    css: "./static/assets/css",
    scss: "./static/assets/scss",
    vendor: "./static/assets/vendor",
  },
};

















// Define your Gulp tasks for Django integration
gulp.task('build:static', function () {
  // Task for compiling Sass
  gulp.src('sass/**/*.scss')
    .pipe(sass())
    .pipe(autoprefixer())
    .pipe(gulp.dest('css'));

  // Task for minifying JavaScript
  gulp.src('js/src/**/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('js/dest'));

  // Additional tasks for other static files (images, fonts, etc.)
  // ...

  // You can also include a task to copy static files to Django's static directory
  gulp.src('static/**/*')
    .pipe(gulp.dest('/static/static'));
});

// Define a default task that runs all the required tasks
gulp.task('default', gulp.series('build:static'));
