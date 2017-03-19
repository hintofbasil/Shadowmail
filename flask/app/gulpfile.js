'use strict';

var browserify = require('browserify');
var gulp = require('gulp');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var gutil = require('gulp-util');
var del = require('del');

var paths = {
  javascript: 'js/**/*'
}

gulp.task('clean', function() {
  return del(['./dist']);
});

gulp.task('homepage-js', function() {
  var b = browserify({
    entries: './js/homepage.js',
    debug: false
  });

  return b.bundle()
    .pipe(source('hompage.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init({loadMaps: true}))
      .pipe(uglify())
      .on('error', gutil.log)
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest('./dist/js/'));
});

gulp.task('javascript', ['homepage-js']);

gulp.task('build', ['javascript'])

gulp.task('watch', function() {
  gulp.watch(paths.javascript, ['javascript']);
});

gulp.task('default', ['watch', 'build']);
