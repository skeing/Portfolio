<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class CurrentDateController extends Controller
{
    public function showCurrentDate()
    {
        $currentDate = date('Y-m-d'); // 今日の日付を取得
        return view('current-date', compact('currentDate'));
    }
}
