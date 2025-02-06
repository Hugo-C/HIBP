# Have I Been Pwned - clone

## Sommaire
1. [Démarche et choix effectués](#démarche-et-choix-effectués)
2. [Architecture](#architecture)
3. [Utilisation](#utilisation)
4. [Limite et améliorations possible](#limite-et-améliorations-possible)

## Démarche et choix effectués

### Gestion de projet

On utilisera [le projet Github](https://github.com/users/Hugo-C/projects/5) pour suivre les tâches à effectuer.
Une CI basique sera mise en place. Uniquement la branche master sera utilisée. On veillera a utiliser des messages de commit clairs. On utilisera la méthode TDD pour écrire et tester le code métier.

Les conventions de code suivi sont:
* [PEP8](https://pep8.org/) pour Python
* [Airbnb](https://github.com/airbnb/javascript) pour JavaScript

### Partie fuite de mot de passe

Pour cette partie on suppose qu'un grand nombre de lecture (requête API) sera faîte comparé aux écritures. On a bien pris en compte la nécessité de garantir la confidentialité des mots de passe recherchés.  

La première étape entreprise est de regarder les choix fait par des solutions similaire. Il se trouve que le site haveibeenpwned.com [explique son fonctionnement](https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/#cloudflareprivacyandkanonymity) et [est partiellement sur Github](https://github.com/HaveIBeenPwned/PwnedPasswordsAzureFunction).
On y apprend que des functions as a service sont utilisées pour récupérer des fichiers dans un service cloud. Par dessus, un CDN est utilisé comme cache. Une des raisons avancé de cette architecture est la maitrise des coûts. On va de notre coté rester sur une solution qui ne dépend pas d'un fournisseur cloud.  
Sur le site, la confidentialité des mots de passes est assurée par l'utilisation du préfixe d'un hash. Cela permet d'envoyer seulement quelques bytes de donnée commun à de multiples passwords. On constate que c'est la même méthode utilisée par [Google Safe Browsing](https://developers.google.com/safe-browsing/v4#update-api-v4). On retient donc cette façon de faire.

Pour le choix de la fonction de hachage, on retient MD5 et [xxHash](https://github.com/Cyan4973/xxHash) comme potentiel candidat de part leur rapidité d'éxécution. Effectivement, on n'a pas besoin d'une fonction de hachage cryptographique, mais seulement qu'elle soit à sens unique, pour la confidentialité des passwords soumit, et qu'elle est une bonne uniformité en sortie pour répartir les données en DB. Les collisions ne sont pas un problème ici, car on cherche au contraire à en générer en utilisant le préfixe.   
On test les deux fonctions via un [benchmark](doc/benchmark.py) en utilisant 15 caractère comme taille de mot de passe de façons arbitraire:
```
$ pyperf timeit -s 'import benchmark; p = benchmark.random_password(15)' 'benchmark.hash_md5(p)'
.....................
Mean +- std dev: 782 ns +- 18 ns
```
vs
```
pyperf timeit -s 'import benchmark; p = benchmark.random_password(15)' 'benchmark.hash_xxh(p)'
.....................
Mean +- std dev: 403 ns +- 12 ns
```
Le gain étant relativement important (~50% plus rapide), on choisi d'utiliser xxHash. 

> A noter que je m'étais trompé à cette étape, en incluant la génération du mot de passe dans le benchmark, ce qui faussait la comparaison avec MD5 qui n'était plus lent que de seulement 6%.  
> Avec un si faible écart MD5 aurait était retenu étant donné qu'il est bien plus répandu.  

On va utiliser comme préfixe les 5 premiers caractères hexadécimaux des hashes, ce qui donne 16<sup>5</sup>=1 048 576 combinaisons possibles. On devrait ainsi avoir en moyenne un peu moins de 14 mots de passes retournés avec la liste rockyou utilisé.

Pour la base de donnée il nous faut donc un moyen d'associer un préfixe de hash à un ensemble de mot de passe à la manière d'une HashMap. Cela permet de faire le gros du travail une seule fois à l'initialisation et d'ensuite répondre au client rapidement. Au vu de la quantité de donnée (14 millions de mots de passe) et du fait que certains préfixe seront sans doute demandé plus que d'autre, on préfère ne pas les stocker en mémoire. Cela élimine comme option une HashMap dans le code et dans une certaine mesure Redis. Une base SQL type PostgreSQL a été considérée, avec des rows qui pourrait ressembler à `<Password as Primary Key> | <Hash prefix>`. En utilisant un index sur le préfixe et en utilisant la bonne taille de varchar les performances doivent être acceptable pour ce jeu de donnée. Cependant on suppose qu'on voudra ajouté d'autres sources de données plus tards et donc cette solution n'est pas idéale.  
On propose d'utiliser [Kvrocks](https://github.com/apache/kvrocks) qui est une surcouche de [rocksdb](https://rocksdb.org/). Cette base de donnée clé-valeur est compatible avec le protocole Redis et utilise un stockage sur disque. De plus, elle intégre nativement [un cache LRU](https://github.com/facebook/rocksdb/wiki/Block-Cache#lru-cache) ce qui est particulièrement adapté à notre situation et simplifie l'architecture global en enlevant le besoin d'avoir un cache dédié.

Pour le backend on utilise Python et FastAPI pour une question de simplicité de ces outils.

---

<details>
  <summary>Détails de certains problèmes rencontrés</summary>

<h4>Initialisation lente de la base de donnée</h4>

Lors de la création du script d'initialisation, arrive le moment de faire le premier test avec le jeu de données complet (au niveau de ce <a href="https://github.com/Hugo-C/HIBP/commit/7f5db7e5eecfada55918ec67b2e98cba9b911c9e">commit</a> )). Le script est relativement lent et je l'arrete après quelques minutes. En essayant sur 100k entrées le script prend 34s, ce qui donnerai 80mins avec les 14M d'entrées.
J'utilise un outil de profiling (en l'occurrence Sentry car je l'avais sous la main). Il montre que plus de 90% du temps est passé dans <code>PasswordStorage.add_password</code>:

![profile Sentry](doc/sentry_profiling.png) 

Plusieurs solutions sont envisagées. La première est de pousser les données en batch, ce qui nécessite avec `sadd` de pousser plusieurs password qui ont le même prefix. Cette solution parait compliqué à mettre en place, car elle oblige a stocker beaucoups d'informations en mémoire. D'autres solutions comme utiliser de l'asynchrone, ou encore du multiprocessing implique une forte complexité supplémentaire. Par exemple découper le fichier d'entrée en une centaine de mini fichiers pour être traité par des "workers" différents. Heureusement Redis fournit un système de batch de commande via [les pipelines](https://redis.io/docs/latest/develop/use/pipelining/) qui permet d'avoir des commandes différentes dans un seul appel. Après quelques essais, des batchs de 200 commandes semble être le bon compromis qui permet de faire 100k passwords en 3s, ce qui est plus acceptable.  
Au final il faut compter 10~15 mins pour inserer la totalité des données. Sur un projet où cette opération serait répété, le choix de la base de donnée et/ou son optimisation pourrait être exploré.

<h4>Nécessité d'utiliser un bundler</h4>

Pour la partie frontend, je n'ai pas réussis à mon grand regret à utiliser la librairie npm dans le navigateur d'une manière compatible avec Jest. Je me suis rabattu sur `browserify` puis sur `esbuild`.  
Cela m'a obligé à supprimer les références au JS dans le HTML et a séparer le JS entre les éléments qui font appel au DOM (non compatible avec Jest) avec le code que l'on souhaite tester (voir [commit](https://github.com/Hugo-C/HIBP/commit/6204d792616d1e2dca3550e355350d4feeee047e)).

</details>

---

### Partie génération de mot de passe

Pour cette fonctionnalité on privilégie sa génération directement sur le navigateur du client. En effet cela garantit la confidentialité du password créé.  
On utilisera comme paramétrage par défaut:
> 15 caractères minimum et contenant des minuscules, des majuscules, des chiffres et des caractères spéciaux.

En s'appuyant sur [les recommandations de l'Anssi datant de 2021](https://cyber.gouv.fr/publications/recommandations-relatives-lauthentification-multifacteur-et-aux-mots-de-passe) pour un niveau de sensibilité fort à très fort.

On utilise la fonction pseudo-aléatoire [Crypto.getRandomValues](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/getRandomValues) qui est adaptée à une utilisation cryptographique.
Pour garantir la présence de certains éléménts comme une majuscule, on relancera la génération du mot de passe jusqu'a ce que toutes les conditions soient remplies.    
Javascript ne semble pas avoir de fonction `shuffle` cryptographique, sinon on aurait pu l'utiliser pour rajouter en premier les éléments requis et ensuite les mélanger. 

## Architecture

![Vue d'ensemble de l'architecture](doc/architecture.excalidraw.png)

## Utilisation

Le projet utilise docker, lancez simplement:
```shell
docker compose up
```
Le site est disponible sur http://localhost:80/ par défaut. Il est utilisable avec une base de donnée non initialisée.

### Initialisation de la base de donnée

Dans un nouveau terminal, si vous avez déjà une base de mot de passe type rockyou.txt en local:
```shell
docker compose run --rm -v <path_to_directory_having_rockyou.txt>:/rockdir fastapi python src/init_scripts/init_db_with_password_file.py /rockdir/rockyou.txt
```
sinon si vous souhaitez le télécharger automatiquement:
```shell
docker compose run --rm fastapi python src/init_scripts/init_db_with_password_file.py --download
```

La base de donnée utilise un volume Docker qui peut être supprimé avec `docker volume remove hibp_kvrocks_data_volume`.

### Setup dev

`poetry sync` permet d'installer les dépendances. L'outils justfile (voir [ici pour l'installation](https://github.com/casey/just?tab=readme-ov-file#cross-platform)) permet de faire tourner les tests et le linter.  
`npm install` permet d'installer les dépendances coté frontend.  
`npm run build` permet de générer les bundles JS utilisé par le front et `npm test` de lancer les tests Jest.

## Limite et améliorations possible

Le fichier docker compose est fonctionnel mais pourrait être améliorer pour de la production, notamment en ajoutant un mot de passe à la connection, customiser les paramètres par défaut, utiliser de la réplication pour de la haute disponibilité, ...
Le script d'initialisation s'exécute de manière séquentielle. On peut améliorer les performances en utilisant de l'asynchrone et/ou du multithread pour paralleliser le calcul des hashs et l'insertion en DB au prix d'une plus grande complexité du code.