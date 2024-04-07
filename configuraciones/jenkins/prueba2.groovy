
def gitGetTags(){
    try {
        def gettags = ('git ls-remote -t https://github.com/alejandrofm98/restaurantqr-backend.git').execute()
        def tags = gettags.text.readLines().collect { it.split()[1].replaceAll('refs/tags/', '').replaceAll('\\^\\{}', '')}.unique()
        tags = tags.sort {s-> s.size()}.reversed()
        for (int x = tags.size()-1; x >= 10; x--){
            tags.remove(x)
        }
        def proyectName = "demo-"
        def firstValueNumber = tags.first.replace(proyectName,"").split("\\.")
        tags.add(0,proyectName+firstValueNumber[0]+"."+firstValueNumber[1]+"."+(firstValueNumber[2].toInteger()+1).toString())
        if (Entorno.equals("desarrollo"))
            tags = tags.collect(){it+"-SNAPSHOT"}
        return tags
    }catch (Exception e) {
        return [e.dump()]
    }
}

println(gitGetTags())


//ArrayList<String> array = new ArrayList<String>();
//array.add("demo-0.0.10-SNAPSHOT");
//array.add("demo-0.0.12-SNAPSHOT");
//array.add("demo-0.0.11-SNAPSHOT");
//array.add("demo-0.0.9-SNAPSHOT");
//array.add("demo-0.0.20-SNAPSHOT");
//array.add("demo-0.0.8-SNAPSHOT");
//array.add("demo-0.0.131-SNAPSHOT");
//
//array.sort(Comparator.nullsFirst(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder())).reversed());
//
//println(array)
