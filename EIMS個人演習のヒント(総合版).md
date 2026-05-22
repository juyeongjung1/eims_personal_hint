# EIMS個人演習のヒント（総合版）

## 演習1.1 のヒント

### 仕様確認

この演習では、タイピング練習で使う「問題の一覧」を配列で用意し、その中身を順番に表示します。

問題文では、次の2つを実装することが求められています。

| やること | 内容 |
| --- | --- |
| 問題数を表示する | 配列に入っている問題が何個あるかを表示する |
| 問題を表示する | 配列の中身を先頭から順番に表示する |

つまり、難しい処理を作るというより、「配列を作る」「配列の個数を調べる」「配列の中身を1つずつ取り出す」練習です。

※「Java によるデータ構造とアルゴリズム」 154～159ページ を参照してください。

### 1. まず、問題を配列に入れる

タイピングの問題は1つだけではなく、複数あります。

複数の文字列をまとめて持ちたいときは、`String[]` の配列を使います。

```java
String[] keywords = { "class", "int", "boolean", "if", "while" };
```

この1行は、次のように分けて読むと分かりやすいです。

| 部分 | 意味 |
| --- | --- |
| `String[]` | 文字列を複数入れられる配列 |
| `keywords` | 配列の変数名 |
| `{ ... }` | 配列の中に入れる値の一覧 |
| `"class"` など | 実際のタイピング問題 |

`{}` の中には、問題にしたい文字列をカンマ `,` で区切って並べます。

### 2. 問題数を表示する

配列に入っている要素の数は、`配列名.length` で取得できます。

この演習では、`keywords` という配列を作っているので、問題数は次のように取得します。

```java
keywords.length
```

注意してください。配列の要素数は、`length()` ではありません。

| 書き方 | 正しいか | 理由 |
| --- | --- | --- |
| `keywords.length` | 正しい | 配列の要素数を表すプロパティ |
| `keywords.length()` | 間違い | 配列では `length()` メソッドを使わない |

文字列と組み合わせると、実行例のように「5個の問題があります」と表示できます。

```java
System.out.println(keywords.length + "個の問題があります");
```

### 3. 配列の中身を1つずつ表示する

問題数を表示したら、次は配列の中身を1つずつ表示します。

ここでは、拡張for文を使います。

```java
for (String word : keywords) {
    System.out.println(word);
}
```

この文は、次のように読むと分かりやすいです。

```text
keywords の中から、1つずつ取り出す。
取り出した1つ分の値を、word という変数に入れる。
word を表示する。
```

`for (String word : keywords)` の各部分は、次の意味です。

| 部分 | 意味 |
| --- | --- |
| `String` | 取り出す値の型。今回は文字列 |
| `word` | 取り出した1つ分の値を入れる変数 |
| `keywords` | 取り出し元の配列 |

たとえば、`keywords` に5つの文字列が入っている場合、`word` の中身は次のように変わります。

| 繰り返し | `word` に入る値 |
| ---: | --- |
| 1回目 | `"class"` |
| 2回目 | `"int"` |
| 3回目 | `"boolean"` |
| 4回目 | `"if"` |
| 5回目 | `"while"` |

### 仕上げの考え方

この演習で一番大事なのは、次の順番です。

| 順番 | やること | 確認すること |
| ---: | --- | --- |
| 1 | `String[]` で問題の配列を作る | 5つの文字列が入っているか |
| 2 | `keywords.length` で問題数を取得する | `5` が取れるか |
| 3 | 拡張for文で配列から1つずつ取り出す | `word` に順番に値が入るか |
| 4 | `System.out.println(word)` で表示する | 5つの問題が1行ずつ表示されるか |

配列は「複数の値をまとめて入れる箱」、拡張for文は「箱の中身を先頭から1つずつ取り出す仕組み」と考えると、流れをつかみやすくなります。

## 演習1.2 のヒント

### 仕様確認

この演習では、ミリ秒で表された処理時間を、人が読みやすい文字列に変換します。

たとえば `12345678` ミリ秒をそのまま表示しても、どれくらいの時間なのかすぐには分かりません。

そこで、次のように変換します。

```text
12345678ミリ秒 → 3時間25分45秒678
```

問題文では、`getStringScore(long score)` というメソッドを作り、ミリ秒の値を「○時間×分△秒□□□」形式の文字列にして返すことが求められています。

※「アルゴリズム演習」 演習1.3 の問題と似ています。

### 1. まず、`getStringScore` の役割を整理する

いきなりコードを書き始める前に、このメソッドが何をするものなのかを分けて考えましょう。

`getStringScore(long score)` の役割は、次の2つです。

| 役割 | 内容 |
| --- | --- |
| 単位に分ける | `score` を「時間」「分」「秒」「ミリ秒」に分解する |
| 文字列にする | `0` の単位を省略しながら、表示用の文字列を作る |

ポイントは、計算と表示を一度に考えないことです。

まずは数字を分解します。そのあとで、分解した数字を使って文字列を作ります。

### 2. 「余り」と「商」を使って単位を分ける

ミリ秒を時間・分・秒・ミリ秒に分けるには、割り算 `/` と余り `%` を使います。

- 余り（`%`）: 小さい単位だけを取り出す
- 商（`/`）: 大きい単位にまとめる

たとえば、`12345` ミリ秒を考えます。

`12345 % 1000` は `345` です。これは「1000ミリ秒で割り切れずに残った部分」なので、ミリ秒部分になります。

`12345 / 1000` は `12` です。これは「12345ミリ秒の中に、1秒が12個入っている」という意味です。

```longdivision
dividend=12345
divisor=1000
quotient=12
product=12000
remainder=345
formula=12345 ÷ 1000 = 12 あまり 345
note=`12345 % 1000` は、この筆算の「あまり」である `345` を取り出す計算です。
```

このように、`%` は今見ている単位の残りを取り出すために使い、`/` は次の大きな単位へ進むために使います。

### 3. 各変数の役割を確認する

計算は、ミリ秒 → 秒 → 分 → 時間の順番で進めると考えやすいです。

```java
long msec = score % 1000;       // ① 1000で割った余り → ミリ秒部分
long secScore = score / 1000;   // ② 何秒分あるか

long sec = secScore % 60;       // ③ 60で割った余り → 秒部分
long minScore = secScore / 60;  // ④ 何分ぶんあるか

long min = minScore % 60;       // ⑤ 60で割った余り → 分部分
long hour = minScore / 60;      // ⑥ 残った商 → 時間部分
```

ここで大切なのは、途中の値にも名前を付けていることです。

たとえば、`secScore` は「何秒分あるか」を表す値です。`minScore` は「何分ぶんあるか」を表す値です。

このように一時変数を使うと、「今はどの単位で考えているのか」が分かりやすくなります。

`score / 1000 / 60` のように式を長くつなげることもできますが、初心者のうちは途中の値を変数に入れて、1段階ずつ確認する方が安全です。

`12345678` ミリ秒の場合、各変数の値は次のようになります。

| 変数名 | 計算式 | 値 | 解説 |
| --- | --- | ---: | --- |
| `msec` | `score % 1000` | 678 | 1000で割った余り → 「ミリ秒部分」だけ取り出す |
| `secScore` | `score / 1000` | 12345 | 12345秒ぶんあることを表す |
| `sec` | `secScore % 60` | 45 | 60で割った余り → 「1分未満の秒」だけ取り出す |
| `minScore` | `secScore / 60` | 205 | 205分ぶんあることを表す |
| `min` | `minScore % 60` | 25 | 60で割った余り → 「1時間未満の分」だけ取り出す |
| `hour` | `minScore / 60` | 3 | 残った3時間を、時間単位で取っておく |

### 4. 0の単位は表示しない

単位に分けられたら、次は文字列を作ります。

ただし、問題文には「各単位の値が0の部分を含まない文字列」とあります。

つまり、計算した値を全部そのままつなげてはいけません。

たとえば `score = 123456`（約2分）を変換すると、次のようになります。

- `hour = 0` → 「0時間」は不要
- `min = 2` → 「2分」だけは表示したい

もし `if (hour > 0)` の条件がないと、「0時間2分3秒456」のように、不要な `0時間` が表示されてしまいます。

```text
12345678 ミリ秒は、3時間25分45秒678
1234567 ミリ秒は、20分34秒567      ← hour=0 ⇒ 「時間」部分をスキップ
123456 ミリ秒は、2分3秒456          ← hour=0, secScore=123 ⇒ 「秒」も残る
12345 ミリ秒は、12秒345             ← hour=0, min=0 ⇒ 「分」をスキップ
```

出力する・しないの判断は、次のように整理できます。

| 単位 | 変数 | 表示する条件 | 表示例 |
| --- | --- | --- | --- |
| 時間 | `hour` | `hour > 0` のときだけ | `3時間` |
| 分 | `min` | `min > 0` のときだけ | `25分` |
| 秒 | `sec` | `sec > 0` のときだけ | `45秒` |
| ミリ秒 | `msec` | `msec > 0` のときだけ | `678` |

ポイントは、先頭から順番に「必要な単位だけ」を文字列へ追加していくことです。

```text
hour が 0 より大きい？ → はい：時間を追加 / いいえ：何もしない
min  が 0 より大きい？ → はい：分を追加   / いいえ：何もしない
sec  が 0 より大きい？ → はい：秒を追加   / いいえ：何もしない
msec が 0 より大きい？ → はい：ミリ秒を追加 / いいえ：何もしない
```

文字列を作るときは、最初に空文字を用意して、条件に合う単位だけ追加します。

```java
String strScore = "";

if (hour > 0) {
    strScore += hour + "時間";
}

if (min > 0) {
    strScore += min + "分";
}

// 秒、ミリ秒も同じ考え方で追加する
```

`+=` は、今ある文字列の後ろに文字を追加する書き方です。

最初は `strScore` が空なので、時間があれば時間を追加し、分があればその後ろに分を追加します。

### 5. `main` メソッドですること

`main` メソッドでは、`getStringScore` が正しく動くかを確認します。

問題文では、繰り返しを用いて、引数の値を10分の1にしながら複数回 `getStringScore` を呼び出すように指定されています。

```java
long score = 12345678;

for (int i = 0; i < 4; i++) {
    System.out.println(score + "ミリ秒は、" + getStringScore(score));
    score /= 10;
}
```

この `for` 文は、同じメソッドをいろいろな大きさのスコアで試すための確認用です。

`score /= 10;` は、`score = score / 10;` と同じ意味です。

毎回スコアを小さくすることで、時間が出る場合、時間が出ない場合、分が出ない場合などをまとめて確認できます。

| 繰り返し | 表示に使う `score` | 確認したいこと |
| ---: | ---: | --- |
| 1回目 | `12345678` | 時間・分・秒・ミリ秒がすべて出るか |
| 2回目 | `1234567` | 時間が0のとき、時間を出さないか |
| 3回目 | `123456` | 分・秒・ミリ秒だけで表示できるか |
| 4回目 | `12345` | 分が0のとき、分を出さないか |

### 仕上げの考え方

この演習で一番大事なのは、次の順番です。

| 順番 | やること | 何が分かるか |
| ---: | --- | --- |
| 1 | ミリ秒から、ミリ秒部分を取り出す | `msec` の値 |
| 2 | 残りを「何秒ぶんあるか」にする | `secScore` の値 |
| 3 | 秒部分を取り出す | `sec` の値 |
| 4 | 残りを「何分ぶんあるか」にする | `minScore` の値 |
| 5 | 分部分を取り出す | `min` の値 |
| 6 | 残った値を時間として扱う | `hour` の値 |
| 7 | 0ではない単位だけを文字列に追加する | 表示用の文字列 |

一気に完成させようとすると難しく見えますが、やっていることは「単位を1つずつ分ける」「必要なものだけ表示する」の2つです。

まずは変数 `msec`, `sec`, `min`, `hour` に期待した値が入るかを確認し、その後で文字列を組み立ててください。

## 演習2.1 のヒント

### 仕様確認

この演習では、演習1.1で作った「問題の配列」を使い、入力された文字列と各問題が等しいかを確認します。

タイピング練習アプリでは、ユーザが入力した文字列と、出題された問題が一致しているかを判定する必要があります。

演習2.1で作る処理は、次の流れです。

| 順番 | やること | 例 |
| ---: | --- | --- |
| 1 | 問題の配列を用意する | `"class"`, `"int"`, `"boolean"` など |
| 2 | 比較対象の文字列を用意する | `"boolean"` |
| 3 | 配列から問題を1つずつ取り出す | `word` に1つずつ入る |
| 4 | 比較対象と問題を比較する | `input` と `word` を比べる |
| 5 | 等しいか、等しくないかを表示する | `等しいです` / `等しくないです` |

※「Java によるオブジェクト指向プログラミング」 105～107ページ を参照してください。

### 1. 演習1.1から増えるもの

演習1.1では、配列の中身を表示するだけでした。

演習2.1では、そこに「比較対象の文字列」が増えます。

```java
String[] keywords = { "class", "int", "boolean", "if", "while" };
String input = "boolean";
```

`keywords` は問題の一覧です。

`input` は、ユーザが入力した文字列の代わりです。今回は動作確認のために、最初から `"boolean"` を入れておきます。

### 2. 文字列は `equals()` で比較する

ここが一番大事です。

Javaで文字列の中身を比較するときは、`==` ではなく `equals()` を使います。

| 書き方 | 意味 | この演習で使うか |
| --- | --- | --- |
| `input == word` | 同じものを指しているかを比べる | 使わない |
| `input.equals(word)` | 文字列の中身が同じかを比べる | 使う |

たとえば、`input` が `"boolean"`、`word` が `"boolean"` のとき、`input.equals(word)` は `true` になります。

```java
if (input.equals(word)) {
    System.out.println("等しいです");
} else {
    System.out.println("等しくないです");
}
```

`if` の条件式には、「等しいときに `true` になる式」を書きます。

### 3. 配列の中身を1つずつ比較する

配列の中身を1つずつ取り出すところは、演習1.1と同じです。

```java
for (String word : keywords) {
    System.out.print(input + "と" + word + "は、");

    if (input.equals(word)) {
        System.out.println("等しいです");
    } else {
        System.out.println("等しくないです");
    }
}
```

`System.out.print()` は、改行せずに表示します。

その後の `System.out.println()` で「等しいです」または「等しくないです」を表示すると、実行例と同じ1行になります。

| `word` の値 | `input.equals(word)` | 表示される結果 |
| --- | --- | --- |
| `"class"` | `false` | `booleanとclassは、等しくないです` |
| `"int"` | `false` | `booleanとintは、等しくないです` |
| `"boolean"` | `true` | `booleanとbooleanは、等しいです` |
| `"if"` | `false` | `booleanとifは、等しくないです` |
| `"while"` | `false` | `booleanとwhileは、等しくないです` |

### 仕上げの考え方

この演習で一番大事なのは、次の順番です。

| 順番 | やること | 確認すること |
| ---: | --- | --- |
| 1 | 問題の配列を作る | 5つの文字列が入っているか |
| 2 | 比較対象の文字列を作る | 配列のどれか1つと同じ値にする |
| 3 | `keywords.length` で問題数を表示する | `5個の問題があります` と表示されるか |
| 4 | 拡張for文で問題を1つずつ取り出す | `word` に順番に値が入るか |
| 5 | `input.equals(word)` で比較する | `"boolean"` のときだけ等しいになるか |

演習1.1に「文字列比較」が1つ追加された、と考えると理解しやすくなります。

## 演習2.2 のヒント

### 仕様確認

この演習では、タイピング結果を表す `Score` クラスを作ります。

演習1.2では、ミリ秒のスコアを表示用の文字列に変換しました。

演習2.2では、その処理を `Score` クラスの中に入れて、次の情報を1つのオブジェクトとして扱えるようにします。

| 情報 | 例 | 役割 |
| --- | --- | --- |
| 名前 | `世界太郎` | 誰のスコアか |
| 数値のスコア | `123456` | ミリ秒のまま保存する値 |
| 表示用スコア | `2分3秒456` | 画面に見せるための文字列 |
| 日付 | `2020/01/01 12:34:56` | いつの記録か |

ポイントは、コンストラクタの引数は3つなのに、フィールドは4つあることです。

4つ目の `score` フィールドは、引数として受け取るのではなく、`longScore` から作ります。

※「Java によるオブジェクト指向プログラミング」 38～41ページ を参照してください。

### 1. `Score` クラスで持つフィールド

仕様にあるフィールドを、まず整理します。

| 種類 | 名前 | 型 | 役割 |
| --- | --- | --- | --- |
| フィールド | `name` | `String` | 入力された名前を保存する |
| フィールド | `longScore` | `long` | ミリ秒のスコアを数値のまま保存する |
| フィールド | `date` | `String` | 記録日時を文字列で保存する |
| フィールド | `score` | `String` | 表示用に変換したスコアを保存する |
| コンストラクタ引数 | `name` | `String` | `this.name` に入れる |
| コンストラクタ引数 | `longScore` | `long` | `this.longScore` に入れ、さらに表示用スコアの変換にも使う |
| コンストラクタ引数 | `date` | `String` | `this.date` に入れる |

フィールドは `private` にします。

これは、クラスの外から直接値を書き換えられないようにするためです。これをカプセル化といいます。

```java
private String name;
private long longScore;
private String date;
private String score;
```

### 2. コンストラクタで何をするか

コンストラクタでは、受け取った値をフィールドに保存します。

ただし、`score` だけは少し特別です。

`score` は引数で受け取るのではなく、`longScore` を `getStringScore(longScore)` で変換して作ります。

データの流れは、次のように考えると分かりやすいです。

```text
longScore（数値のスコア）
    ↓ getStringScore(longScore) で変換
score（表示用の文字列）
    ↓ toString() で名前・日付とつなげる
世界太郎, 2分3秒456, 2020/01/01 12:34:56
```

```java
public Score(String name, long longScore, String date) {
    this.name      = name;
    this.longScore = longScore;
    this.date      = date;
    // ★ここで long → String に変換して score フィールドにセット
    this.score     = getStringScore(longScore);
}
```

`this.name` はフィールドの `name`、右側の `name` はコンストラクタの引数です。

同じ名前なのでややこしいですが、`this.` が付いている方が「このオブジェクトが持っているフィールド」です。

| 書き方 | 意味 |
| --- | --- |
| `name` | コンストラクタで受け取った引数 |
| `this.name` | `Score` オブジェクトが持つフィールド |

### 3. `getStringScore` は演習1.2の再利用

演習1.2で作成した `getStringScore(longScore)` を、`Score` クラスの中に移します。

`score` フィールドは、`〇時間〇分〇秒〇〇〇` という文字列を入れるためのフィールドです。コンストラクタの引数として受け取る値は `long` 型の数字ですが、コンストラクタの中で `getStringScore(longScore)` を呼び出す処理をすると、`long` の数字が演習1.2のように変換され、戻り値として取得されます。

その戻り値を `score` フィールドに代入しておくと、出力用の文字列の値をセットできます。

このメソッドは、`Score` クラスの内部で表示用スコアを作るために使います。

そのため、外から自由に呼び出す必要はありません。`private` にして、クラスの中だけで使うメソッドにします。

```java
private static String getStringScore(long score) {
    // 演習1.2で作った変換処理をここに入れる
}
```

### 4. getter メソッドを作る

フィールドを `private` にしたので、外から値を取り出すためのメソッドを用意します。

それが getter メソッドです。

| メソッド | 返すフィールド | 戻り値の型 |
| --- | --- | --- |
| `getName()` | `name` | `String` |
| `getLongScore()` | `longScore` | `long` |
| `getDate()` | `date` | `String` |
| `getScore()` | `score` | `String` |

戻り値を間違えると、あとでこのクラスを使うときに期待した値が取り出せなくなります。

### 5. `toString` で表示形式を作る

※「Java によるオブジェクト指向プログラミング」 38～41ページ を参照してください。

実行例のように出力するために、一番簡単な方法が `toString` メソッドを再定義することです。

```text
世界太郎, 2分3秒456, 2020/01/01 12:34:56
```

```java
@Override
public String toString() {
    // ★カンマと空白の位置を実行例と同じに
    return name + ", " + score + ", " + date;
}
```

`System.out.println(s);` のように `Score` オブジェクトをそのまま表示すると、Javaは自動的に `toString()` を呼び出します。

そのため、`toString()` の戻り値を実行例と同じ形にしておけば、`System.out.println(s);` だけで次のように表示できます。

```text
世界太郎, 2分3秒456, 2020/01/01 12:34:56
```

### 仕上げの考え方

この演習で一番大事なのは、次の順番です。

| 順番 | やること | 確認すること |
| ---: | --- | --- |
| 1 | `typing` パッケージに `Score` クラスを作る | `package typing;` があるか |
| 2 | 4つのフィールドを `private` で用意する | `name`, `longScore`, `date`, `score` があるか |
| 3 | コンストラクタで3つの引数を受け取る | 名前、数値スコア、日付を受け取れるか |
| 4 | `score` は `getStringScore(longScore)` で作る | 表示用スコアになっているか |
| 5 | getterを作る | 各フィールドを返せるか |
| 6 | `toString()` を作る | 実行例と同じ形式で表示できるか |

演習1.2で作った「ミリ秒を文字列に変換する処理」が、ここで `Score` クラスの一部として再利用されます。

## 演習2.3 のヒント

### 仕様確認

この演習では、処理時間を測る `Stopwatch` クラスを作ります。

演習1.2では「ミリ秒を表示用文字列に変換する処理」を作りました。

演習2.3では、その元になる「何ミリ秒かかったか」という数値を測定します。

`Stopwatch` クラスでやることは、次の3つです。

| メソッド | 役割 |
| --- | --- |
| `start()` | 開始時刻を保存する |
| `stop()` | 終了時刻を保存する |
| `getLongScore()` | `終了時刻 - 開始時刻` を返す |

※「Java によるオブジェクト指向プログラミング」 98～102ページ を参照してください。

### 1. まず、時間計測の考え方を整理する

時間を測るときは、開始時刻と終了時刻を記録します。

たとえば、次のようなイメージです。

| タイミング | 保存する値 | 例 |
| --- | --- | ---: |
| 処理の前 | `start` | 1000 |
| 処理の後 | `end` | 1032 |
| かかった時間 | `end - start` | 32ミリ秒 |

つまり、処理時間は `end - start` で求めます。

### 2. Java API で `System` クラスを調べる

ブラウザで `java api` と検索し、Oracle の Java API ドキュメントを開きます。

| 操作 | 見る場所 | 確認すること |
| --- | --- | --- |
| `java api` と検索する | 検索結果 | Oracle の Java API ドキュメントを選ぶ |
| APIページを開く | ページ上部または右上 | クラス検索欄を探す |
| 日本語表示にしたい場合 | ブラウザ翻訳 | メソッド説明を読みやすくする |

APIページの検索欄へ `System` と入力し、候補に出る `java.lang.System` を選択します。

探したいのは、現在時刻をミリ秒で取得するメソッドです。

```text
検索欄に入力する文字: System
選択する候補: java.lang.System
探したいメソッド: currentTimeMillis()
```

### 3. `currentTimeMillis()` をコードで使う

ブラウザの翻訳Onを推奨します。

`System` クラスのメソッド一覧で、`currentTimeMillis()` を探します。次の点を確認してください。

| 見るポイント | 意味 |
| --- | --- |
| `static` | インスタンスを作らず、`System.currentTimeMillis()` と呼び出せる |
| 戻り値 `long` | ミリ秒の時刻は `long` 型で受け取る |
| メソッド名 `currentTimeMillis()` | 現在時刻をミリ秒で取得する |

APIで見つけた情報をコードに直すと、次の1行になります。

```java
long now = System.currentTimeMillis();
```

`static` が付いているので、`new System()` のようにインスタンスを作る必要はありません。

`System.currentTimeMillis()` と書けば、現在時刻をミリ秒で取得できます。

### 4. `start()` と `stop()` で時刻を保存する

`Stopwatch` クラスには、開始時刻と終了時刻を保存するフィールドを用意します。

```java
private long start;
private long end;
```

`start()` では、現在時刻を `start` フィールドに保存します。

`stop()` では、現在時刻を `end` フィールドに保存します。

```java
public void start() {
    // ★開始時刻をミリ秒で取得
    start = System.currentTimeMillis();
}

public void stop() {
    // ★終了時刻をミリ秒で取得
    end = System.currentTimeMillis();
}
```

### 5. 経過時間を計算する

```java
public long getLongScore() {
    // ★end - start の符号ミスに注意
    return end - start;
}
```

`getLongScore()` では、`end - start` を返します。

`start - end` にするとマイナスの値になってしまうので、順番に注意してください。

| 式 | 結果 |
| --- | --- |
| `end - start` | 正しい。かかった時間になる |
| `start - end` | 間違い。マイナスになりやすい |

### 6. `Ex2_3` で動作確認する

`Ex2_3` の `main` で「0～999を出力するのに何ミリ秒かかったか」を測定します。

呼び出す順番は、次の通りです。

| 順番 | やること | 目的 |
| ---: | --- | --- |
| 1 | `Stopwatch` のインスタンスを作る | 時間を測る道具を用意する |
| 2 | `start()` を呼ぶ | 測定開始 |
| 3 | `for` 文で0～999を表示する | 測定したい処理 |
| 4 | `stop()` を呼ぶ | 測定終了 |
| 5 | `getLongScore()` を呼ぶ | かかったミリ秒を取得する |

```java
Stopwatch s = new Stopwatch();
s.start();

// ここに、時間を測りたい処理を書く

s.stop();
System.out.println(s.getLongScore() + "ミリ秒");
```

`stop()` を呼ぶ位置が早すぎると、測りたい処理が含まれません。

逆に、`stop()` の後に測りたい処理を書いても、その処理時間は測定されません。

### 仕上げの考え方

この演習で一番大事なのは、次の順番です。

| 順番 | やること | 確認すること |
| ---: | --- | --- |
| 1 | `typing` パッケージに `Stopwatch` クラスを作る | `package typing;` があるか |
| 2 | `start` と `end` フィールドを用意する | どちらも `long` 型か |
| 3 | `start()` で開始時刻を保存する | `start` に現在時刻が入るか |
| 4 | `stop()` で終了時刻を保存する | `end` に現在時刻が入るか |
| 5 | `getLongScore()` で差分を返す | `end - start` になっているか |
| 6 | `Ex2_3` で呼び出す | `start()` → 処理 → `stop()` の順か |

演習2.2の `Score` は「スコア情報を保存するクラス」、演習2.3の `Stopwatch` は「スコアの元になる時間を測るクラス」です。

この2つが後のタイピングアプリで組み合わさっていきます。

## 演習3.1 のヒント

### 仕様のポイント

キーボードから文字を入力してもらい、`return` する `KB` クラスの `readLine()` メソッドを定義します。

`BufferedReader` + `InputStreamReader(System.in)` や、`Scanner` で標準入力を1行読んで返します。

※「Java システムプログラミング」 42～49ページ を参照してください。

例外処理をしないとエラーになるので、`try-catch` で例外処理をしてください。

### 入力受付ループの注意点

```java
while (true) {
    System.out.print("何か入力(exitで終了)> "); // 入力を促す文字列
    String input = KB.readLine();
    // ★"exit" と比較するときは equals() を使う
    if ("exit".equals(input)) {
        break;
    }
    System.out.println(input);
}
```

## 演習3.2 のヒント

### 仕様のポイント

事前に `keywords.txt` を Eclipse のプロジェクト内に格納してください。

※「Java システムプログラミング」 28～29ページ を参照してください。

`TypingFile.read(String filename)` はクラスメソッドとして定義し、引数で渡されたファイル名のテキストを1行ずつ `ArrayList<String>` に追加して返します。

`ArrayList` に格納する理由は、入力を複数してもらうので、複数のデータを格納する必要があるからです。

### `TypingFile.java` の要点抜粋

```java
public static ArrayList<String> read(String filename) {
    ArrayList<String> list = new ArrayList<>();
    // ★try-with-resources で自動クローズ
    try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
        String line;

        // この部分に以下のコードを書きましょう。
        // 1. 1行ずつ読んで null までループする。
        // 2. 読んだ文字列は list.add(line) しておくコード
    }

    return list;
}
```

例外処理は `try-with-resources` と `e.printStackTrace()` を使い、必ずリソースを解放するようにします。

### 動作確認例（`Ex3_2` の `main` 内）

`keywords.txt` は、Eclipseプロジェクト内の一番上位に配置しないといけません。誤字に気を付けてください。

```java
ArrayList<String> data = TypingFile.read("keywords.txt");
for (String s : data) {
    System.out.println(s); // ★ファイルの各行が順に表示されるか確認
}
```

`static` クラスメソッドを呼び出すので、クラス名.メソッド名で呼び出します。

## 演習3.3 のヒント

### 仕様のポイント

`Typing` クラスの `main()` では、以下の順序で各クラスを組み合わせます。

### 1. 問題読み込み

```java
ArrayList<String> keywords = TypingFile.read("keywords.txt");
```

### 2. 名前入力

```java
System.out.print("名前を入力> ");
String name = KB.readLine();
```

### 3. 練習開始待ち

```java
System.out.print("何かキーを押してください（タイピング練習開始）> ");
KB.readLine(); // ★何でも良いので1行読み込む
```

### 4. 時間計測開始

```java
Stopwatch sw = new Stopwatch();
sw.start();
```

### 5. 問題ループ

```java
while (keywords.size() > 0) {
    // ★残り問題数を表示する
    // ヒント：keywords.size() を文字列とつなげる
    System.out.println("あと" + keywords.____() + "問");

    // ★先頭の問題を表示して、入力を1行受け取る
    // ヒント：リストの0番目は keywords.get(0)
    System.out.print(keywords.____(0) + "> ");
    String line = KB.readLine();

    // ★文字列の比較なので == ではなく equals を使う
    // ヒント：line と keywords.get(0) を比較する
    if (line.equals(____)) {
        // ★正解なら、出題済みの先頭問題を削除する
        keywords.remove(____);

        // ★残り問題の出題順をランダム化する
        Collections.shuffle(____);
    } else {
        // ★不正解時のメッセージを表示する
        System.out.println("____");
    }
}
```

ここでは、変数名が混ざりやすいです。問題リストは `keywords`、入力された文字列は `line` と考えると整理しやすくなります。

実行例:

```text
...
...
あと 1問
byte> byte
終了！
世界太郎さんの結果：15秒948
```

### 6. 時間計測終了＆結果を `Score` に記録。結果表示

```java
// ★時間計測を止める
sw.stop();

// ★名前、計測結果、任意の日付文字列を使って Score を作る
// ヒント：new Score(名前, long型のスコア, 任意の文字列)
Score s = new Score(____, sw.getLongScore(), "now");

// ★終了メッセージと結果を表示する
System.out.println("終了！");
System.out.println(name + "さんの結果：" + s.____());

// ここに、結果を出力するコードを書いてください。
```

この問題の実行例では、時間まで出力しなくても良いので、コンストラクタの第3引数には、任意の文字列を入れておけばOKです。

## 演習4.1 のヒント

### 仕様のポイント

`root` ユーザで MySQL に接続し、データベースとアプリ用ユーザを作成します。

### 注意点

- `-p` オプション直後にパスワードが続く書式を守る
- SQL文は必ずセミコロン（`;`）で終了する
- エラーが出た際は、妥協せず正しくもう一回入力すること

## 演習4.2 のヒント

### 仕様のポイント

`typinguser` で接続し、`score` テーブルを自動採番付き主キーで作成します。

```sql
-- ① typinguser でログイン
mysql -utypinguser -ppassword

-- ② 使用 DB 指定
USE typingdb;

-- ③ テーブル作成
CREATE TABLE score (
    no INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20),
    score INT,
    datetime DATETIME
);

-- ④ 構造確認
DESC score;
exit;
```

### 注意点

- `AUTO_INCREMENT` を指定しないと主キーは自動採番されない
- `VARCHAR(20)` の文字数制限を超えないよう注意

## 演習4.3 のヒント

### 仕様のポイント

`INSERT` → `SELECT` → `UPDATE` → `DELETE` と順に操作を行い、結果を確認します。

※「データベース入門」の2章を参照してください。

```sql
-- ① レコード追加（現在日時は NOW()）
INSERT INTO score(name, score, datetime)
VALUES('たろう', 123456, NOW());

-- ② 登録確認
SELECT * FROM score;

-- ③ ソート表示（スコア小→大）
SELECT name, score, datetime
  FROM score
 ORDER BY score;

-- ④ 名前の更新
UPDATE score
   SET name = '太郎'
 WHERE name = 'たろう';

-- ⑤ レコード削除
DELETE FROM score
 WHERE name = '太郎';

exit;
```

SQLは、先に `SELECT` で現在の状態を確認してから `UPDATE` や `DELETE` を実行すると安心です。特に `WHERE` 句は「どの行だけを対象にするか」を決める部分なので、対象の名前を正確に確認してください。

### 注意点

- `NOW()` は MySQL の現在日時関数
- `WHERE` 条件を誤ると大量削除・更新になるため慎重に指定
- `SELECT *` は簡易確認用。実務では必要なカラムのみ指定すると可読性向上

## 演習5.1 のヒント

### 仕様のポイント

- MySQL Connector を必ずビルドパスに登録しておくこと
- `ScoreDAO` クラスのフィールドに JDBC の接続情報を持たせる（`url`, `user`, `pass`）
- 問題文で提示している接続情報に誤字がないか、しっかり確認してください
- `connectTest()` は `DriverManager.getConnection(...)` で接続し、「接続しました。」を出力、必ず切断する（`try-with-resources`）

※「Java データベースプログラミング」 35ページ を参照してください。

```java
public void connectTest() {
    // ★ここで DB に接続してからメッセージを出す
    // ヒント：引数は ScoreDAO のフィールド url, user, pass を使う
    try (Connection con = DriverManager.getConnection(url, ____, ____)) {
        // ★接続できたことが分かるメッセージを表示する
        System.out.println("接続しました。");
    } catch (SQLException e) {
        e.printStackTrace(); // ★例外時は必ずスタックトレース
    }
}
```

動作確認の際は、`ScoreDAO` のインスタンスを生成し、`connectTest` メソッドを呼び出してください。

## 演習5.2 のヒント

### 仕様のポイント

- `select()` メソッドを追加し、`score` テーブルから `name`, `score`, `datetime` を取得、`Score` オブジェクトに詰めて `ArrayList<Score>` で返す。
- SQLは `"SELECT name, score, datetime FROM score ORDER BY score"`、`Statement` + `ResultSet` で処理、必ず接続を閉じること。

※「Java データベースプログラミング」 142～146ページ を参照してください。

※追加で、演習ガイド5.1の解答のソースコードも参照してください。

```java
public ArrayList<Score> select() {
    String sql = "SELECT name, score, datetime FROM score ORDER BY score";
    ArrayList<Score> list = new ArrayList<>(); // ★リストのインスタンスを予め宣言（空っぽのリスト生成）

    // ヒント：接続情報はフィールドの url, user, pass を使う
    try (Connection con = DriverManager.getConnection(url, ____, ____)) {
        // ★SQLを実行するための Statement を作る
        Statement stmt = con.createStatement();

        // ★SELECT文を実行すると、結果は ResultSet として返ってくる
        // ヒント：SELECT用の実行メソッド。executeUpdate ではありません。
        ResultSet rs = stmt.____(sql);

        // ★次の行がある間だけループする
        while (rs.next()) {
            // ★ResultSet から name, score, datetime を取り出す
            // ヒント：列名はSQL文の SELECT の後に書いた名前と同じ
            String name = rs.getString("____");
            long sc = rs.getLong("____");
            String dt = rs.getString("____");

            // ★取り出した3つの値で Score インスタンスを作る
            // ヒント：Scoreの引数は「名前、long型スコア、日付文字列」の順
            Score s = new Score(name, ____, ____);

            // ★作成した Score を list に追加する
            list.add(s);
        }
    } catch (SQLException e) {
        e.printStackTrace();
    }

    return list; // ★複数の記録が入っているリストを、main メソッドへ return する
}
```

迷ったときは、次の順で1行ずつ確認してください。

1. SQL文だけを見て、取得する列名が `name`, `score`, `datetime` の3つだと確認する
2. `ResultSet` から取り出す型を、`String`, `long`, `String` に分けて考える
3. 取り出した値を `Score` のコンストラクタの引数順に並べる
4. 最後に、作った `Score` を `ArrayList` に追加する

### 動作確認例（`Ex5_2` Main メソッド）

```java
ScoreDAO dao = new ScoreDAO();

// ★dao.select() の戻り値を拡張 for 文で1件ずつ取り出す
for (Score s : dao.select()) {
// ★取り出した Score を表示する
    System.out.println(____);
}
```

```text
さぶろう, 1分40秒200, 2023-02-02 12:34:56
じろう, 2分30秒123, 2023-01-01 00:00:00
```

## 演習5.3 のヒント

### 仕様のポイント

`insert(Score score)` メソッドを追加し、`PreparedStatement` で `name` と `score` をバインド、`datetime` は `now()` で現在日時を自動設定します。

SQLは `"INSERT INTO score (name, score, datetime) VALUES (?, ?, now())"` です。

必ず接続を閉じ、例外時はトレース出力します。

```java
public void insert(Score score) {
    String sql = "INSERT INTO score (name, score, datetime) VALUES (?, ?, now())";

    // ヒント：接続情報はフィールドの url, user, pass を使う
    try (Connection con = DriverManager.getConnection(url, ____, ____)) {
        // ★? つきのSQLを実行するので PreparedStatement を作る
        PreparedStatement ps = con.prepareStatement(sql);

        // ★1つ目の ? には名前を入れる
        // ヒント：Score から名前を取得する getter を使う
        ps.setString(1, score.____());

        // ★2つ目の ? には long 型のスコアを入れる
        // ヒント：Score から long 型スコアを取得する getter を使う
        ps.setLong(2, score.____());

        // ★INSERT文を実行する
        // ヒント：INSERT/UPDATE/DELETE用の実行メソッドです。
        ps.____();
    } catch (SQLException e) {
        e.printStackTrace();
    }
}
```

`?` の順番と `setXxx` の番号は対応しています。1番目の `?` が名前、2番目の `?` がスコアです。`datetime` はSQLの `now()` が入れるため、Javaから値を渡す必要はありません。

### 動作確認例（`Ex5_3`）

```java
ScoreDAO dao = new ScoreDAO();

// ★テスト用の Score を1件作る
Score score = new Score("____", ____, "test");

// ★insert メソッドでDBに登録する
dao.insert(____);

// ★select メソッドで登録後の一覧を表示する
for (Score s : dao.select()) {
    System.out.println(____);
}
```

既存のランキングに「シロー, 3時間25分45秒678, …」が追加されます。

## 演習5.4 のヒント

### 仕様のポイント

今まで実装したパーツを、組み立てれば完成です。

1. 演習3.3のソースコードでタイピング測定をする
2. 演習5.3の `insert` メソッドを呼び出し、DBにタイピング結果を記録する
3. 演習5.2の `select` メソッドを呼び出し、`return` される `ArrayList` の記録データを、拡張for文で出力します

`Score` オブジェクト生成時の時間は、任意の文字列（`now` など）で大丈夫です。登録される時は、演習5.3で作った通りに、MySQL の `now()` 関数で現在の時間が登録されるからです。

登録後、`dao.select()` で取得した `ArrayList<Score>` をループ出力し、ヘッダ `*** ランキング ***` を付けます。

```java
// タイピング処理後…
// ★時間計測を止める
stopwatch.stop();

// ★計測結果から Score を作る
// ヒント：名前は入力済みの name、スコアは stopwatch から取得する
Score score = new Score(____, stopwatch.getLongScore(), "now");

// ★DB 登録
// 1. ScoreDAO のインスタンスを作る
ScoreDAO dao = new ScoreDAO();
// 2. insert メソッドに、作成した Score を渡す
dao.insert(____);

// ★ランキング表示
// 1. 見出しを表示する
System.out.println("*** ランキング ***");
// 2. select メソッドで一覧を取得する
// 3. 拡張 for 文で1件ずつ表示する
for (Score s : dao.select()) {
    System.out.println(____);
}
```

ここでは「タイピング結果を表示する処理」と「DBに登録してランキングを表示する処理」を分けて考えると整理しやすいです。まずコンソールに結果が出ることを確認し、その後でDB登録、最後にランキング表示を足してください。

実行例:

```text
終了！
世界太郎さんの結果：17秒11
*** ランキング ***
世界太郎, 17秒11, 2023-03-02 15:25:50
さぶろう, 1分40秒200, 2023-02-02 12:34:56
```

上記ポイントをヒントに、「これまで作成した `KB`, `TypingFile`, `Stopwatch`, `Score` クラス」と組み合わせて実装を進めてください。

特に、DB接続 → 登録 → 検索 → 表示の流れを一連で通す位置と、例外処理・リソース解放の確実性に注意すると全体がスムーズに動作します。
