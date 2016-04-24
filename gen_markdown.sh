folders=`ls -1 -d */`
for f in $folders;
do
    rm $f/Readme.md
    jpgs=`ls -1v $f/*.jpg`
    for j in $jpgs;
    do
        line=`echo $j|sed 's|//|/|g'`
        echo "![](../$line)" >> $f/Readme.md
    done
    echo ''
done
