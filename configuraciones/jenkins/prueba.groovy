def gitGetTags() {
    try {
        def gettags = ('git ls-remote -t https://github.com/alejandrofm98/restaurantqr-backend.git').execute()
        def tags = gettags.text.readLines().collect { it.split()[1].replaceAll('refs/tags/', '').replaceAll('\\^\\{}', '')}.unique()
        def proyectName = "demo-"
        def lastValueNumbers = tags.last.replace(proyectName,"").split("\\.")
        tags.add(proyectName+lastValueNumbers[0]+"."+lastValueNumbers[1]+"."+(lastValueNumbers[2].toInteger()+1).toString())
        if (params.Entorno.equals("desarrollo"))
            tags = tags.reverse().collect(){it+"-SNAPSHOT"}
        return tags
    }catch (Exception e) {
        return [e.dump()]
    }
}

println(gitGetTags())
