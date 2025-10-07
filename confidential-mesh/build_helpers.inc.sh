######
# include for functions and variables

###
# Key=Value set to setup mesh of services
f_MESH="mesh.txt"

###
# function to obtain value of a key from a Key=Value text file and fail if no key exists of is duplicate
# Example: export RELEASE=${RELEASE:="$(get_value MESH_PREFIX $f_MESH)"}
# This command will look for the key MESH_PREFIX in $f_MESH and set RELEASE to MESH_PREFIX's value, unless RELEASE is already set.
function get_value {
    test 1 -eq `grep -c "^${1}=" ${2}` && {
        test -n "$(grep "^${1}=" ${2} |tail -1 |cut -d '=' -f 2-)" && {
            grep "^${1}=" ${2} |tail -1 |cut -d '=' -f 2-
        } || {
            false
        }
    } || {
        echo "..:ERR: $2 has no unique value for $1" >/dev/stderr;
        false
    }
}
