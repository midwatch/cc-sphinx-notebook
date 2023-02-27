echo "Update PATH"
echo 'PATH="/usr/local/bin:$PATH"' >> /home/$USER/.profile
echo 'PATH="/vagrant/bin:$PATH"' >> /home/$USER/.profile

echo "install sphinx-notebook via pipx"
python3 -m pipx install sphinx-notebook
python3 -m pipx ensurepath

echo "Cache github ssh fingerprint"
sh -c "ssh -T git@github.com -o StrictHostKeyChecking=no; true"
