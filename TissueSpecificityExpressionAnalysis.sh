# Author: ZhangJie
# Update time: 20211117 pm

# Usage: bash TissueSpecificityExpressionAnalysis.sh /PATH_INPUT/ [Option] /PATH_OUTPUT/
# For example: bash TissueSpecificityExpressionAnalysis.sh /PATH_INPUT/ ProteinCodingGenes /PATH_OUTPUT/

## Input file
# For example: ProteinCodingGenesExpressionMatrix.tsv
# Format: ChromNum\tChromStart\tChromEnd\tGeneName\tFPKM\tType (Type: Protein_coding-Brain)
path_input=$1 #/PATH_INPUT
type_input=$2 #Option: ProteinCodingGenes

## Output
path_output=$3 #/PATH_OUTPUT

### ------------- Code body --------------

if [ ! -d ${path_output}/tmp ]
then  mkdir -p ${path_output}/tmp
fi

#### ------------ Main --------------
time less ${path_input}/${type_input}ExpressionMatrix.tsv | sed '1d' | awk '{print $4}' | sort | uniq | while read line;do
	max=$(less ${path_input}/${type_input} | sed '1d' | awk '{if($4=="'"${line}"'") print $0}' | awk 'BEGIN {max = 0} {if ($5+0 > max+0) max=$5} END {print max}')
	min=$(less ${path_input}/${type_input} | sed '1d' | awk '{if($4=="'"${line}"'") print $0}' | awk 'BEGIN {min = 10000000000000} {if ($5+0 < min+0) min=$5} END {print min}')
	diff=$(echo "scale=5;${max}-${min}" | bc)
	echo "${line} ${diff}" >> ${path_output}/${type_input}TissueSpecificityMetrics.tsv
done

sed -i 's/ /\t/g' ${path_output}/${type_input}TissueSpecificityMetrics.tsv

# The "file_output" will be to plot the boxplot using R.
