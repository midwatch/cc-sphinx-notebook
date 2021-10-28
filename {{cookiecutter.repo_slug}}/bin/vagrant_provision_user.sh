echo "Update PATH"
echo 'PATH="/usr/local/bin:$PATH"' >> /home/$USER/.profile
echo 'PATH="/vagrant/bin:$PATH"' >> /home/$USER/.profile

echo "Cache github ssh fingerprint"
sh -c "ssh -T git@github.com -o StrictHostKeyChecking=no; true"
