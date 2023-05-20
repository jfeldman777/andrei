const gulp = require('gulp');
const sass = require('gulp-sass');
const autoprefixer = require('gulp-autoprefixer');
const uglify = require('gulp-uglify');

 //Задача для компиляции Sass
 gulp.task('sass', function () {
   return gulp.src('sass/**/*.scss')
     .pipe(sass())
     .pipe(autoprefixer())
     .pipe(gulp.dest('css'));
 });

 // Задача для минификации JavaScript
 gulp.task('uglify', function () {
   return gulp.src('js/src/**/*.js')
     .pipe(uglify())
     .pipe(gulp.dest('js/dest'));
 });

// Задача по умолчанию, выполняющая задачи 'sass' и 'uglify'
gulp.task('default', gulp.parallel('sass', 'uglify'));
/////////////////////////////////////////////////////////////////////
gulp.task("scss", function () {
  return gulp
    .src([
      paths.src.scss + "/custom/**/*.scss",
      paths.src.scss + "/portal/**/*.scss",
      paths.src.scss + "/portal.scss",
    ]) 
    
    
    .pipe(wait(500))
    .pipe(sourcemaps.init())
    .pipe(sass().on("error", sass.logError))
    .pipe(
      autoprefixer({
        overrideBrowserslist: ["> 1%"],
      })
    )
    .pipe(sourcemaps.write("."))
    .pipe(gulp.dest(paths.src.css))
    .pipe(browserSync.stream());
});
