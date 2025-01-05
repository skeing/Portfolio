<!DOCTYPE html>
<htmL>
    <head>
        <title>Portfolio</title>
        <meta name="description" content="このページはポートフォリオ用のサンプルです。">
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>{{$title}}</h1>
        <p><p>{!! $text !!}</p></p>
        <img src="{{ asset('images/sample.jpg') }}" alt="サンプル画像"><br>
        <a href="https://x.com/samuraijuku">私のプロフィールはこちら</a>
        <p>※このページはポートフォリオ用のサンプルです。</p>
    </body>
</htmL>