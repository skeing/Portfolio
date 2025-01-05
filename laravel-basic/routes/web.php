<?php

use Illuminate\Support\Facades\Route;
//　ルーティングを設定するコントローラを宣言する
use App\Http\Controllers\HelloController;
use App\Http\Controllers\CurrentDateController;
use App\Http\Controllers\StaticPageController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::get('/hello', [HelloController::class, 'index']);

Route::get('/current-date', [CurrentDateController::class, 'showCurrentDate']);

Route::get('/portfolio', [StaticPageController::class, 'portfolio']);