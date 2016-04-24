folders=`ls -1 -d */`
for f in $folders;
do
    jpgs=`ls -1v $f/*.jpg`
    for j in $jpgs;
    do
        line=`echo $j|sed 's|//|/|g'`
        echo "![GitHub Logo]($line)" >> $f/Readme.md
    done
    echo ''
done
