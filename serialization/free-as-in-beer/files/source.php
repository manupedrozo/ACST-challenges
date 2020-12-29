 I'd just like to interject for a moment. What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. 
Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, 
shell utilities and vital system components comprising a full OS as defined by POSIX.

Many computer users run a modified version of the GNU system every day, without realizing it. 
Through a peculiar turn of events, the version of GNU which is widely used today is often called "Linux", 
and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.

There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: 
the program in the system that allocates the machine's resources to the other programs that you run. 
The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. 
Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. 
All the so-called "Linux" distributions are really distributions of GNU/Linux.
<?php
/*
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

[
BLABLABLA we get it...
]

For more information on this, and how to apply and follow the GNU GPL, see
<http://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<http://www.gnu.org/philosophy/why-not-lgpl.html>.

*/?><?php

Class GPLSourceBloater{
    public function __toString()
    {
        return highlight_file('license.txt', true).highlight_file($this->source, true);
    }
}


if(isset($_GET['source'])){
    $s = new GPLSourceBloater();
    $s->source = __FILE__;

    echo $s;
    exit;
}

$todos = [];

if(isset($_COOKIE['todos'])){
    $c = $_COOKIE['todos'];
    $h = substr($c, 0, 32);
    $m = substr($c, 32);

    if(md5($m) === $h){
        $todos = unserialize($m);
    }
}

if(isset($_POST['text'])){
    $todo = $_POST['text'];

    $todos[] = $todo;
    $m = serialize($todos);
    $h = md5($m);

    setcookie('todos', $h.$m);

    header('Location: '.$_SERVER['REQUEST_URI']);
    exit;
}

?>
<html>
<head>
    <style>
    * {font-family: "Comic Sans MS", cursive, sans-serif}
    </style>
</head>

<h1>My open/libre/free/PHP/Linux/systemd/GNU TODO List</h1>
<a href="?source"><h2>It's super secure, see for yourself</h2></a>
<ul>
<?php foreach($todos as $todo):?>
    <li><?=$todo?></li>
<?php endforeach;?>
</ul>

<form method="post" href=".">
    <textarea name="text"></textarea>
    <input type="submit" value="store">
</form>

