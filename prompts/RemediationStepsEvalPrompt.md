# Remediation Steps Evaluation Prompt

```text
You will be shown an AI-generated JSON insight enclosed in the <insight></insight> tags containing two fields: `investigation_summary` and `remediation_steps`.

Evaluate the quality of `remediation_steps` and classify the insight into one of the following categories: [Good, Needs Improvement, Bad].

Rate based on the following criteria:
- For PHP FPM-related issues (like OOM due to memory spikes), does the insight properly identify processes using commands like `ps aux | grep php-fpm` or `htop`?
- The insight should not recommend users to directly view or edit the configuration files like `fpm-pool.conf`, Varnish `.vcl`, Elasticsearch `jvm.options` files. Instead it should guide the users to the relevant UI sections. And suggest contacting hashlify support for further investigation and resolution of the issue.
- It must not recommend restarting services (PHP FPM, MySQL, Elasticsearch, Varnish) using systemctl or CLI. It should instead guide users to the **Manage Services** section in the UI.
- The insight should not suggest customers to stop MySQL (MariaDB) service as it is the database service and cannot be stopped by anyone. Also the insight can only suggest stopping the Varnish, Redis, and New Relic Services and that too only from the **Server > Manage Services** section from the UI and not via direct CLI over SSH in case the issue resolution depends on stopping these services.
- No misleading or impossible actions from the client end (e.g., stopping MySQL service, modifying debian-sys-maint settings, adjusting attributes like `pm.max_children`, `-Xms`, `-Xmx`, `output_buffering`, changing configuration files from the `etc/**/*.*` directory via SSH etc). Instead the insight should recommend the client to contact hashlify support for issue resolution.
- Does not suggest installing unrelated external services (e.g., Elasticsearch when the issue is PHP FPM-related).
- All suggestions should follow the UI paths and support hashlify procedures.
- The insight should not suggest modifying any file(s) / folder(s) except from the `public_html`, `private_html`, `<application_identifier>/tmp` folders via CLI over SSH. The user can only edit files in the mentioned three folders via CLI over SSH. (The <application_identifier> is unique identifier for each user's application (like `zwtafadysi`, `agfvcbysir`))
- If the insight contains suggestions of editing or updating files in the `public_html`, `private_html`, `<application_identifier>/tmp` folders like `cat /home/35219.hashlifystagingapps.com/pkvetxqpzb/public_html/wp-content/debug.log`, `nano /home/35219.hashlifystagingapps.com/pkvetxqpzb/public_html/wp-config.php` essentially any files in the `public_html` folder with path like `/home/<server_url>/<application_identifier>/public_html/**/*.*`, `private_html` folder with path like `/home/<server_url>/<application_identifier>/private_html/**/*.*` and `tmp` folder with path like `/home/<server_url>/<application_identifier>/tmp/*.*` then for all such files the insight should recommend editing or updating these files via CLI through SSH instead of suggesting the users to edit/update these files via UI as files in these three folders can only be updated via SSH. 
- Does not recommend installing 3rd-party WordPress plugins.
- If cron jobs are involved, they should be created using the **Cron Management** tab in the UI (not external cron tools).
- If large files/folders are recommended for deletion, the insight must:
  - Recommend taking a local backup before deletion.
  - Suggest horizontal/vertical scaling if the user chooses not to delete them.
- Avoids mentioning unrelated stack components. E.g., doesn't mix Laravel log issues with WordPress configs.
- If the issue is due to large logs or disk saturation:
  - Insight should recommend **Disk Cleanup** from UI (`Settings & Packages > Optimization`) and NOT deletion via SSH.
  - If a service is down due to full disk, remediation must include which files/folders are consuming the most space.
- No false/misleading remediations (e.g., suggesting bot blocking when there's minimal bot activity, Redis config changes for MariaDB issues, etc.).
- Should NOT recommend features/tools deprecated or not supported by hashlify (e.g. Bot Protection).
- If the insight relates to a specific application, it must mention the **application identifier**.
- The insight should not suggest the user to view or modify the following files: 
    - '/var/log/apache2'
    - '/var/log/chrony'
    - '/var/log/imunify360'
    - '/var/log/mysql'
    - '/var/log/private'
    - '/var/log/redis'
    - '/var/log/unattended-upgrades'
    - '/var/log/varnish'
- If it highlights a DDoS risk:
  - The IPs listed in the remediation must match those in the investigation.
  - Only malicious IPs should be mentioned, not legit user or bot IPs.
  - It must not recommend blocking legitimate bots (e.g., Google or Bing bots).

Format the output as JSON with the following keys:
classification: "One of: Good | Needs Improvement | Bad",
justification: "Explain which criteria were satisfied or violated."

Now evaluate the following insight:

<insight>
    {insight}
</insight>

{format_instructions} 