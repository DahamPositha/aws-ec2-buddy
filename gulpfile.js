
let babel = require('gulp-babel'),
    sourcemaps = require('gulp-sourcemaps'),
    gulp = require('gulp'),
    es6Path = 'src/**/*.js',
    compilePath = 'dist';

gulp.task('babel', function () {
    gulp.src([es6Path])
        .pipe(sourcemaps.init())
        .pipe(babel())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(compilePath));
});

gulp.task('default', ['babel']);
