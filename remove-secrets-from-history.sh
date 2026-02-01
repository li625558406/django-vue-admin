#!/bin/bash
# 清理 Git 历史中的敏感信息
# 警告：这将重写 Git 历史，请确保在操作前备份！

echo "================================"
echo "清理 Git 历史中的敏感 API Key"
echo "================================"
echo ""
echo "警告：此操作将重写 Git 历史！"
echo "建议：1. 先备份仓库"
echo "      2. 确保所有协作者知道此操作"
echo ""
read -p "是否继续？(yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "操作已取消"
    exit 0
fi

echo ""
echo "开始清理..."

# 方法：使用 git filter-branch 移除 server/.env 的历史
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch server/.env" \
  --prune-empty --tag-name-filter cat -- --all

echo "清理完成！"
echo ""
echo "下一步操作："
echo "1. 检查状态: git status"
echo "2. 强制推送: git push origin --force --all"
echo "3. 通知所有协同志重新克隆仓库"
echo ""
echo "如果仓库是公开的，API Key 可能已经泄露，请立即更换！"
