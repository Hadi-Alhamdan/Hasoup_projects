function BubbleSort(array){
for (let counter = 0 ; counter < array.length -1 ; counter++){
    let swapped = false ;
    for (let elementIndex = 0 ; elementIndex < array.length -1; elementIndex++){
        if (array[elementIndex] > array[elementIndex+1]){
            let temp = array[elementIndex] ;
            array[elementIndex] = array[elementIndex+1];
            array[elementIndex+1] = temp ;
            swapped = true;
        }
    }
    if(swapped == false){
        return array ;
    }
}}



let x  =[ 64, 34, 25, 12, 22, 11, 90 ];
console.log(BubbleSort(x));