'use strict';

var browserify = require('browserify');
var gulp = require('gulp');
var concatCss = require('gulp-concat-css');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var gutil = require('gulp-util');
var del = require('del');
var fs = require('fs');
var sass = require('gulp-sass');

var paths = {
  js: 'js/**/*.js',
  sass: 'sass/**/*.scss',
}

gulp.task('sass', function() {
  return gulp.src(paths.sass)
    .pipe(sass().on('error', sass.logError))
    .pipe(concatCss('bundle.css'))
    .pipe(gulp.dest('static/css'))
});

gulp.task('clean', function() {
  return del(['./static']);
});

gulp.task('javascript-dev', function() {
  return browserify({
    entries: paths.app_js,
    debug: true
  })
  .transform('babelify', {presets: ['es2015']})
  .bundle()
  .pipe(source('bundle.js'))
  .pipe(buffer())
  .pipe(gulp.dest('static/js'))
});

gulp.task('javascript-prod', function() {
  process.env.NODE_ENV = 'production';

  return browserify({
    entries: paths.app_js,
    debug: false
  })
  .transform('babelify', {presets: ['es2015']})
  .bundle()
  .pipe(source('bundle.js'))
  .pipe(buffer())
  .pipe(uglify())
    .on('error', gutil.log)
  .pipe(gulp.dest('static/js'))
});

gulp.task('dev', ['javascript-dev', 'sass'])

gulp.task('prod', ['javascript-prod', 'sass'])

gulp.task('watch', function() {
  gulp.watch(paths.js, ['javascript-dev']);
  gulp.watch(paths.app_js, ['javascript-dev']);
  gulp.watch(paths.sass, ['sass']);
});

gulp.task('default', ['watch', 'dev']);
