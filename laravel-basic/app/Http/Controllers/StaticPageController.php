<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class StaticPageController extends Controller
{   
    // resources/views/portfolio.blade.php を表示
    public function portfolio()
    {
        $title = "私の趣味";
        $text = "私は中学時代にサッカーを始めました。<br>
    現在はサッカーのコーチとして活動をして、趣味のサッカーを楽しんでいます。";
        return view('portfolio', ['text' => $text, 'title' => $title]);

    }
}
