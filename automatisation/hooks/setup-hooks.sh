#!/bin/bash
print_section() {
    echo ""
    echo "=================================================="
    echo " $1"
    echo "=================================================="
}


print_section "Installation des hooks..."

cp automatisation/hooks/post-merge .git/hooks/post-merge
chmod +x .git/hooks/post-merge