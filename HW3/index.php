<?php
//API keys
//Yandex
$YANDEX_TRANSLATE_KEY = '';
$YANDEX_DICTIONARY_KEY = '';

//Google
$api_key_google = '';

//Bing
if (!defined('ACCOUNT_KEY')) {
    define('ACCOUNT_KEY', '');
}
//source language
$to = 'ru';
//target language
$from = 'en';

//жесткий словарь. Заполнить из файла

$myFile = "dictionary.txt";
$fh = fopen($myFile, 'r');
$theData = fread($fh, filesize($myFile));
$assoc_array = array();
$my_array = explode("\n", $theData);
foreach ($my_array as $line) {
    $tmp = explode(" - ", $line);

    if (trim($tmp[0]) == "")
        continue;
    if (trim($tmp[1]) == "")
        continue;

    $tmp[0] = strtolower($tmp[0]);
    $tmp[1] = strtolower($tmp[1]);

    $tmp[0] = str_replace('.', '', $tmp[0]); //удаляем точки
    $tmp[0] = str_replace(',', '', $tmp[0]); //удаляем запятые
    $tmp[0] = str_replace('\"', '', $tmp[0]); //удаляем запятые
    $tmp[0] = str_replace('\'', '', $tmp[0]); //удаляем запятые


    $tmp[1] = str_replace('.', '', $tmp[1]); //удаляем точки
    $tmp[1] = str_replace(',', '', $tmp[1]); //удаляем запятые
    $tmp[1] = str_replace('"', '', $tmp[1]); //удаляем запятые
    $tmp[1] = str_replace('\'', '', $tmp[1]); //удаляем запятые


    $assoc_array[$tmp[0]] = $tmp[1];
}
fclose($fh);

// well the op wants the results to be in $codes
$dictionary = $assoc_array;


/* $dictionary["account"] = "счет"; */
//$dictionary["earn "] = "получить доход";
$dictionary["income"] = "доход";
$dictionary["tool"] = "инструмент";

function GoogleTranslate($api_key, $text, $target, $source = false) {
    $url = 'https://www.googleapis.com/language/translate/v2?key=' . $api_key . '&q=' . rawurlencode($text);
    $url .= '&target=' . $target;
    if ($source)
        $url .= '&source=' . $source;

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    $obj = json_decode($response, true); //true converts stdClass to associative array.
    return $obj;
}
?>


<html>

    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <?php
        if (isset($_GET["q"])) {
            $q = $_GET["q"] . " ";
            $best = $_GET["best"];
        } else {
            $q = "Savings Account is a profitable and convenient tool. You want to earn an income, but not sure if you want to commit funds for the long term. You want to periodically add to the account to grow your savings. You want to be able to withdraw money without losing previously accrued interest.  ";
            $best = "yandex";
        }
        ?>

        <form action="index.php" method="GET">
            Translate:<br>

            <textarea name="q" rows="6" cols="100"><?php echo $q; ?></textarea>
            <input type="submit" value="Translate!">

        </form>

        <?php
        /*
         * To change this license header, choose License Headers in Project Properties.
         * To change this template file, choose Tools | Templates
         * and open the template in the editor.
         */

//if (isset($_GET["q"]))
        {

            $sourseText = $q;
            $sourseText1 = $sourseText;

            $lastPos = -1; //позиция в строке, где мы в последний раз заменили слово из жесткого словаря
            $concurrentWordsNumber = 0;

            //переводим
//Google 
            $obj = GoogleTranslate($api_key_google, $sourseText, $to, $from);
            if ($obj != null) {
                if (isset($obj['error'])) {
                    echo "Error is : " . $obj['error']['message'];
                } else {
                    $automaticallyTranslatedText["Google"] = $obj['data']['translations'][0]['translatedText'];
                    //  if(isset($obj['data']['translations'][0]['detectedSourceLanguage'])) //this is set if only source is not available.
                    //    echo "Detecte Source Languge : ".$obj['data']['translations'][0]['detectedSourceLanguage'];     
                }
            } else {
                //   echo "UNKNOW ERROR";
            }

            //Yandex Translator

            $ch = curl_init();
            $curlConfig = array(
                CURLOPT_URL => "https://translate.yandex.net/api/v1.5/tr.json/translate?key=" . $YANDEX_TRANSLATE_KEY . "&lang=" . $from . "-" . $to . "&text=" . $sourseText,
                CURLOPT_POST => true,
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_POSTFIELDS => array(
                    'field1' => 'some date',
                    'field2' => 'some other data',
                )
            );
            curl_setopt_array($ch, $curlConfig);
            $resultFromYandex = curl_exec($ch);
            curl_close($ch);

            $json = json_decode($resultFromYandex, true);
            $automaticallyTranslatedText["Yandex"] = $json["text"][0] . " ";


//Bing Translator

            require_once('config.inc.php');
            require_once('class/ServicesJSON.class.php');
            require_once('class/MicrosoftTranslator.class.php');

            $translator = new MicrosoftTranslator(ACCOUNT_KEY);

            $text_to_translate = $sourseText;
            $translator->translate($from, $to, $text_to_translate);

            $json = json_decode($translator->response->jsonResponse, true);
            $automaticallyTranslatedText["Bing"] = $json["translation"] . " ";
            $resultTranslation = "";


            $q = preg_match_all("/(.+?)(\.|\?|!|:){1,}(\s|<br(| \/)>|<\/p>|<\/div>)/is", $automaticallyTranslatedText["Google"] . " ", $g1);
            $q = preg_match_all("/(.+?)(\.|\?|!|:){1,}(\s|<br(| \/)>|<\/p>|<\/div>)/is", $automaticallyTranslatedText["Yandex"] . " ", $y1);
            $q = preg_match_all("/(.+?)(\.|\?|!|:){1,}(\s|<br(| \/)>|<\/p>|<\/div>)/is", $automaticallyTranslatedText["Bing"] . " ", $b1);
            ?>
            <hr>

            <table border="1" width="100%" style="table-layout: fixed"> 

                <tr><td width="100%">Source</td><td width="100%">Google</td><td width="100%">Yandex</td><td width="100%">Bing</td></tr>
                <tr><td><?php echo $sourseText; ?></td><td><?php
        foreach ($g1[0] as &$value) {
            echo $value . "<br />";
        }
            ?></td><td><?php
                        foreach ($y1[0] as &$value) {
                            echo $value . "<br />";
                        }
                        ?></td><td><?php
                            foreach ($b1[0] as &$value) {
                                echo $value . "<br />";
                            }
                            ?></td></tr>
                <tr><td>Best Meteor score</td><td><a href="<?php echo basename(__FILE__, '.php') . '.php?best=google&q=' . $sourseText1; ?>">Select</a></td><td><a href="<?php echo basename(__FILE__, '.php') . '.php?best=yandex&q=' . $sourseText1; ?>">Select</a></td><td><a href="<?php echo basename(__FILE__, '.php') . '.php?best=bing&q=' . $sourseText1; ?>">Select</a></td></tr>
            </table>

            <!-- By sentences: <br />
           
           <table border="1" width="100%" style="table-layout: fixed"> 
               
               <tr><td width="100%">Source</td><td width="100%">Google</td><td width="100%">Yandex</td><td width="100%">Bing</td></tr>
               <tr><td><?php
                        foreach ($sourseTextSentences[0] as &$value) {
                            echo $value . "<br />";
                        }
                            ?></td><td><?php echo $automaticallyTranslatedText["Google"]; ?></td><td><?php
            foreach ($automaticallyTranslatedTextSentences["Yandex"][0] as &$value) {
                echo $value . "<br />";
            }
            ?></td><td><?php echo $automaticallyTranslatedText["Bing"]; ?></td></tr>
           </table>-->



            <?php
            if ($best == "google") {
                $automaticallyTranslatedText["Yandex"] = $automaticallyTranslatedText["Google"];
            } else
            if ($best == "bing") {
                $automaticallyTranslatedText["Yandex"] = $automaticallyTranslatedText["Bing"];
            }

            //начинаем алгоритм
            //разбиваем входные тексты на предложения, а предложения - на слова 
            //получаем предложения
            $q = preg_match_all("/(.+?)(\.|\?|!|:){1,}(\s|<br(| \/)>|<\/p>|<\/div>)/is", $sourseText, $sourseTextSentences);

            $q = preg_match_all("/(.+?)(\.|\?|!|:){1,}(\s|<br(| \/)>|<\/p>|<\/div>)/is", $automaticallyTranslatedText["Yandex"] . " ", $automaticallyTranslatedTextSentences["Yandex"]);


            $words = preg_split('/\s+/', $sourseTextSentences[0][0]);
            ?>
            <hr>
            <!-- By sentences: <br />
           
           <table border="1" width="100%" style="table-layout: fixed"> 
               
               <tr><td width="100%">Source</td><td width="100%">Google</td><td width="100%">Yandex</td><td width="100%">Bing</td></tr>
               <tr><td><?php
        foreach ($sourseTextSentences[0] as &$value) {
            echo $value . "<br />";
        }
            ?></td><td><?php echo $automaticallyTranslatedText["Google"]; ?></td><td><?php
            foreach ($automaticallyTranslatedTextSentences["Yandex"][0] as &$value) {
                echo $value . "<br />";
            }
            ?></td><td><?php echo $automaticallyTranslatedText["Bing"]; ?></td></tr>
           </table>-->



    <?php
    $output = "";
    //начинаем алгоритм
    //перебираем предложения

    for ($i = 0; $i < sizeof($sourseTextSentences[0]); $i++) {
        $output.= '<hr>';
        $automaticallyTranslatedTextSentences["Yandex"][0][$i] = str_replace('-', ' - ', $automaticallyTranslatedTextSentences["Yandex"][0][$i]); //удаляем запятые        

        $concurrentWordsNumber = 0;
        $output.="Работаем с предложением <b>" . $sourseTextSentences[0][$i] . "</b>. ";
        $output.="Его перевод <b>" . $automaticallyTranslatedTextSentences["Yandex"][0][$i] . "</b><br/>";

        $noAnyWordFromDictionaryInTheSentence = 1;

//получаем слова для данного предложения

        $wordsSource = preg_split('/\s+/', $sourseTextSentences[0][$i]);

        $wordsTranslatedYandex = preg_split('/\s+/', $automaticallyTranslatedTextSentences["Yandex"][0][$i]);

//удаляем знаки препинания из перевода
        for ($g = 0; $g < sizeof($wordsTranslatedYandex); $g++) {
            $wordsTranslatedYandex[$g] = trim($wordsTranslatedYandex[$g]); //удаляем проблемы с начал и коца слова
            $wordsTranslatedYandex[$g] = strtolower($wordsTranslatedYandex[$g]); //переводим в нижний регистр
            $wordsTranslatedYandex[$g] = str_replace('.', '', $wordsTranslatedYandex[$g]); //удаляем точки
            $wordsTranslatedYandex[$g] = str_replace(',', '', $wordsTranslatedYandex[$g]); //удаляем запятые
        }


        //перебираем слова


        for ($currentWord = 0; $currentWord < sizeof($wordsSource); $currentWord++) {


            //перебираем все последовательности слов с данного слова до конца строки, потом с данного слова до конца строки -1, и так далее до одного данного слова
            for ($wordsNumber = sizeof($wordsSource) - 1; $wordsNumber >= $currentWord; $wordsNumber--) {
                //создать словосочетание

                $collocation = "";
                for ($n = $currentWord; $n < $wordsNumber; $n++) {
                    $collocation.=$wordsSource[$n] . " ";
                }




                $collocation = trim($collocation); //удаляем проблемы с начал и коца слова
                $collocation = strtolower($collocation); //переводим в нижний регистр
                $collocation = str_replace('.', '', $collocation); //удаляем точки
                $collocation = str_replace(',', '', $collocation); //удаляем запятые

                $searchQuery = $collocation;

                //если текущее слово есть в жестком словаре
                if (array_key_exists($searchQuery, $dictionary)) {
                    $noAnyWordFromDictionaryInTheSentence = 0;

                    $output.='<font color="green">Слово <b>' . $searchQuery . '</b> есть в жестком словаре.</font> <br /> ';


                    //но его жесткого перевода нет в текущем переводе предложения



                    $s1 = mb_strtolower($automaticallyTranslatedTextSentences["Yandex"][0][$i], 'UTF-8');
                    $s2 = mb_strtolower($dictionary[$searchQuery], 'UTF-8');
                    $pos = strpos(
                            $s1, $s2
                    );
                 
                    if (
                            $pos === false
                    ) {



                        $output.=$kk . '<font color="orange">Но его жесткого перевода <b>' . $dictionary[$searchQuery] . '</b> нет в текущем переводе предложения <b>' . $automaticallyTranslatedTextSentences["Yandex"][0][$i] . '</b></font><br/>';
                        $output.="Ищем альтернативный перевод слова <b>" . $searchQuery . "</b> с помощью ABBYY: ";


                        //но его синоним там есть
                        //получаем синонимы



                        /*

                          $ch = curl_init();
                          $url = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=" . $YANDEX_DICTIONARY_KEY . "&lang=ru-ru&text=" . $dictionary[$searchQuery];
                          $curlConfig = array(
                          CURLOPT_URL => $url,
                          CURLOPT_POST => true,
                          CURLOPT_RETURNTRANSFER => true,
                          CURLOPT_POSTFIELDS => array(
                          'field1' => 'some date',
                          'field2' => 'some other data',
                          )
                          );
                          curl_setopt_array($ch, $curlConfig);
                          $result = curl_exec($ch);
                          curl_close($ch);


                          $json = json_decode($result, true);

                          // print_r($json["def"][0]["tr"]);

                          // echo "<br/>";
                          $s = $json["def"][0]["tr"][0]["syn"];

                          unset($syn); //обнуляем старый результат
                          foreach ($s as &$value) {
                          $syn[] = $value["text"];
                          }

                         */

//ABBYY
                        /*                 $ch = curl_init();
                          $curlConfig = array(
                          CURLOPT_URL => "http://www.lingvo-online.ru/ru/Translate/en-ru/" . $searchQuery,
                          CURLOPT_POST => true,
                          CURLOPT_RETURNTRANSFER => true,
                          CURLOPT_POSTFIELDS => array(
                          'field1' => 'some date',
                          'field2' => 'some other data',
                          )
                          );
                          curl_setopt_array($ch, $curlConfig);
                          $result = curl_exec($ch);
                          curl_close($ch);


                          $needle = 'showExamp js-show-examples"><span class="translation">';
                          $needle_end = '</span>';
                          $pos = strpos($result, $needle);
                          unset($syn);
                          while ($pos > 0) {

                          $result = substr($result, $pos + strlen($needle));


                          $pos_end = strpos($result, $needle_end);
                          $syn[] = substr($result, 0, $pos_end);


                          $pos = strpos($result, $needle);
                          }
                         * 
                         * 
                         * 
                         */
//if ($searchQuery=="earn")
//$syn[]="зарабатывать";
//получили синонимы для слова $dictionary[$searchQuery]




                        $ch = curl_init();
                        $curlConfig = array(
                            CURLOPT_URL => "http://lingvo.mail.ru/?lang_id=1033&text=" . $searchQuery,
                            CURLOPT_POST => true,
                            CURLOPT_RETURNTRANSFER => true,
                            CURLOPT_POSTFIELDS => array(
                                'field1' => 'some date',
                                'field2' => 'some other data',
                            )
                        );
                        curl_setopt_array($ch, $curlConfig);
                        $result = curl_exec($ch);
                        curl_close($ch);


                        $needle = '<span class="translation">';
                        $needle_end = '</span>';
                        $pos = strpos($result, $needle);

                        if ($pos > 0) {

                            $result = substr($result, $pos + strlen($needle));


                            $pos_end = strpos($result, $needle_end);

                            $translation = substr($result, 0, $pos_end);


                            $pos = strpos($result, $needle);
                        }



                        $translation = str_replace(';', ',', $translation);

                        $translation = explode(',', $translation);

                        $syn = $translation;
                        foreach ($syn as &$value) {


                            $output.= $value . " ";
                        }

                        $output.= "<br />";

                        $b = false;

                        foreach ($syn as &$value)
                            if (in_array($value, $wordsTranslatedYandex)) {
                                $output.= '<font color="green">Синоним <b>' . $value . '</b> есть в данном предложении <b>' . $automaticallyTranslatedTextSentences["Yandex"][0][$i] . '</b>.</font><br />';
                                $b = true;


                                $output.= "Заменяем в переводе слово <b>" . $value . "</b> на его правильный перевод <b>" . $dictionary[$searchQuery] . "</b>. <br />";


                                $automaticallyTranslatedTextSentences["Yandex"][0][$i] = str_replace($value, $dictionary[$searchQuery], $automaticallyTranslatedTextSentences["Yandex"][0][$i]); //удаляем запятые        
                                $lastPos = strpos($automaticallyTranslatedTextSentences["Yandex"][0][$i], $dictionary[$searchQuery]) + strlen($dictionary[$searchQuery]);
                                $concurrentWordsNumber++;

                              
                                break;
                            }

                        if ($b) {
                            $output.= '<font color="blue">Финальный перевод предложения: <b>' . $automaticallyTranslatedTextSentences["Yandex"][0][$i] . '</b> </font><br />';
                        }

                        if (!$b) {
                            $output.= '<font color="red">Ни одного из найденных синонимов слова <b>' . $dictionary[$searchQuery] . '</b> нет в данном предложении <b>' . $automaticallyTranslatedTextSentences["Yandex"][0][$i] . '</b>. </font><br />';

                            if ($concurrentWordsNumber == 1) {
                                //вставляем слово
                                $output.= '<font color="blue">Вставляем слово <b>' . $dictionary[$searchQuery] . '</b> в предложение на позицию <b>' . $lastPos . '</b>, так как это второе слово подряд из словаря, которого нет в предложении</font><br />';

                                $automaticallyTranslatedTextSentences["Yandex"][0][$i] = substr($automaticallyTranslatedTextSentences["Yandex"][0][$i], 0, $lastPos)
                                        . " " .
                                        $dictionary[$searchQuery]
                                        .
                                        substr($automaticallyTranslatedTextSentences["Yandex"][0][$i], $lastPos);


                                $concurrentWordsNumber = 0;
                            }
                          
                        }
                    } else {
                        //если встретили жесткий перевод последовательности 
                        $output.= '<font color="green">Жесткий перевод <b>' . $dictionary[$searchQuery] . '</b> есть в данном предложении <b>' . $automaticallyTranslatedTextSentences["Yandex"][0][$i] . '</b></font><br />';

                       
                    }

                    
                } else {
                    }
            }


         
        }//заканчиваем рассмотрение словосочетания
        $resultTranslation.=$automaticallyTranslatedTextSentences["Yandex"][0][$i] . "<br />";


        if ($noAnyWordFromDictionaryInTheSentence == 1) {
            $output.= '<font color="red">В предложении нет ни одного слова или словосочетания из словаря.</font> <br />';

           
        }
    }//заканчиваем разбор предложения

}
?>

        Перевод: <br />

        <?php
        echo $resultTranslation;
        ?>


        <br /><br />
        <?php
        echo $output;
        ?>

        <br /><br />







    </body>

</html>