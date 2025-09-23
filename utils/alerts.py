import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from datetime import datetime
import os
from dotenv import load_dotenv
import pandas as pd
import json

# Load environment variables
load_dotenv()

class AlertManager:
    """Manager for sending microplastics pollution alerts"""
    
    def __init__(self):
        self.twilio_client = None
        self.smtp_config = None
        self.alert_recipients = []
        self.thresholds = {
            'concentration': 100.0,  # particles/m³
            'hotspot_count': 5,
            'trend_increase': 15.0   # percentage
        }
        
        # Initialize services
        self._init_twilio()
        self._init_email()
        self.load_recipients()
    
    def _init_twilio(self):
        """Initialize Twilio client for SMS alerts"""
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if all([account_sid, auth_token, from_number]):
            try:
                self.twilio_client = Client(account_sid, auth_token)
                self.twilio_configured = True
                print("✅ Twilio SMS alerts configured")
            except Exception as e:
                print(f"⚠️ Twilio configuration error: {e}")
                self.twilio_configured = False
        else:
            self.twilio_configured = False
            print("ℹ️ Twilio not configured - SMS alerts disabled")
    
    def _init_email(self):
        """Initialize email configuration"""
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        
        if all([smtp_server, smtp_port, email_user, email_password]):
            self.smtp_config = {
                'server': smtp_server,
                'port': smtp_port,
                'user': email_user,
                'password': email_password
            }
            self.email_configured = True
            print("✅ Email alerts configured")
        else:
            self.email_configured = False
            print("ℹ️ Email not configured - email alerts disabled")
    
    def load_recipients(self, recipients_file='alert_recipients.json'):
        """Load alert recipients from file"""
        try:
            if os.path.exists(recipients_file):
                with open(recipients_file, 'r') as f:
                    config = json.load(f)
                    self.alert_recipients = config.get('recipients', [])
                    print(f"✅ Loaded {len(self.alert_recipients)} alert recipients")
            else:
                # Default recipients
                self.alert_recipients = [
                    {'name': 'Admin', 'email': 'admin@microplastics.org', 'phone': '+1234567890', 'role': 'admin'},
                    {'name': 'NGO Coordinator', 'email': 'ngo@ocean.org', 'phone': None, 'role': 'ngo'}
                ]
                self.save_recipients(recipients_file)
        except Exception as e:
            print(f"⚠️ Error loading recipients: {e}")
            self.alert_recipients = []
    
    def save_recipients(self, recipients_file='alert_recipients.json'):
        """Save alert recipients to file"""
        try:
            config = {
                'recipients': self.alert_recipients,
                'last_updated': datetime.now().isoformat(),
                'total_recipients': len(self.alert_recipients)
            }
            with open(recipients_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving recipients: {e}")
    
    def send_alert(self, alert_type, location, concentration, region='Unknown', details=''):
        """
        Send alert based on alert type
        
        Args:
            alert_type: 'hotspot', 'threshold', 'trend', 'new_upload'
            location: Location description
            concentration: Measured concentration
            region: Geographic region
            details: Additional information
        """
        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'location': location,
            'concentration': concentration,
            'region': region,
            'details': details
        }
        
        # Generate alert message
        message = self._format_alert_message(alert_data)
        
        # Send through available channels
        success = False
        
        # Email alerts
        if self.email_configured:
            email_success = self._send_email_alert(message, alert_data)
            success = success or email_success
        
        # SMS alerts  
        if self.twilio_configured:
            sms_success = self._send_sms_alert(message, alert_data)
            success = success or sms_success
        
        # Log alert
        self._log_alert(alert_data, success)
        
        return success
    
    def _format_alert_message(self, alert_data):
        """Format alert message for different channels"""
        alert_type = alert_data['type']
        location = alert_data['location']
        concentration = alert_data['concentration']
        region = alert_data['region']
        
        if alert_type == 'hotspot':
            subject = f"🚨 MICROPLASTICS HOTSPOT ALERT: {region}"
            body = f"""
            HOTSPOT DETECTED in {location}, {region}
            
            📊 Current Concentration: {concentration:.1f} particles/m³
    🚩 Risk Level: HIGH - Immediate Action Required
    ⏰ Detected: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Immediate Actions Needed:
    • Coordinate emergency cleanup operations
    • Implement temporary fishing restrictions  
    • Notify local environmental authorities
    • Increase monitoring frequency
    
    View details: https://microplasticsinsight.org/dashboard?region={region}
            """
        
        elif alert_type == 'threshold':
            subject = f"⚠️ THRESHOLD EXCEEDED: {region}"
            body = f"""
            THRESHOLD VIOLATION in {location}, {region}
            
            📈 Concentration: {concentration:.1f} particles/m³
    ⛔ Exceeds threshold of 100 particles/m³ by {concentration-100:.1f}
    📍 Location: {location}
    
    Recommended Actions:
    • Schedule urgent assessment and cleanup
    • Review local pollution sources
    • Update community risk communications
    
    Full report: https://microplasticsinsight.org/reports/{region}
            """
        
        elif alert_type == 'trend':
            subject = f"📈 TREND ALERT: {region}"
            body = f"""
            CONCERNING TREND DETECTED in {region}
            
    📊 {alert_data['details']} increase over past 12 months
    📍 Impacted Area: {location}
    ⚠️ Projected annual increase: {concentration:.1f}%
    
    Proactive Measures Recommended:
    • Review and strengthen prevention programs
    • Increase monitoring in affected areas  
    • Engage stakeholders in policy discussions
    • Prepare additional cleanup resources
    
    Trend analysis: https://microplasticsinsight.org/trends/{region}
            """
        
        elif alert_type == 'new_upload':
            subject = f"🆕 NEW CITIZEN REPORT: {region}"
            body = f"""
            NEW CITIZEN SCIENCE CONTRIBUTION
                        
            👤 Reported by community member
    📷 Photo evidence of plastic debris
    📍 Location: {location}, {region}
    🏷️ Type: {alert_data['details']}
    ⏰ Reported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Actions Required:
    • Verify and validate citizen report
    • Add to official monitoring database
    • Consider for cleanup prioritization
    • Acknowledge contributor publicly
    
    View contribution: https://microplasticsinsight.org/contributions/{alert_data['contribution_id']}
            """
        
        return {
            'subject': subject,
            'body': body.strip(),
            'summary': f"{alert_type.upper()}: {location} - {concentration:.1f} particles/m³"
        }
    
    def _send_email_alert(self, message, alert_data):
        """Send email alert to recipients"""
        try:
            for recipient in self.alert_recipients:
                if not recipient.get('email'):
                    continue
                
                msg = MIMEMultipart()
                msg['From'] = self.smtp_config['user']
                msg['To'] = recipient['email']
                msg['Subject'] = message['subject']
                
                # Email body
                body = f"""
                <html>
                <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #d32f2f;">Microplastics Alert System</h2>
                    
                    <div style="background-color: #f5f5f5; padding: 20px; border-left: 4px solid #d32f2f;">
                        <h3 style="margin-top: 0;">{message['subject']}</h3>
                        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                        <p><strong>Priority:</strong> {self._get_priority(alert_data['type'])}</p>
                        {message['body']}
                        
                        <hr style="margin: 20px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated alert from the Microplastics Insight Platform.<br>
                            For more information: <a href="https://microplasticsinsight.org">Visit Platform</a>
                        </p>
                    </div>
                </div>
                </body>
                </html>
                """
                
                msg.attach(MimeText(body, 'html'))
                
                # Send email
                server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
                server.starttls()
                server.login(self.smtp_config['user'], self.smtp_config['password'])
                text = msg.as_string()
                server.sendmail(self.smtp_config['user'], recipient['email'], text)
                server.quit()
                
                print(f"✅ Email alert sent to {recipient['name']} ({recipient['email']})")
            
            return True
            
        except Exception as e:
            print(f"❌ Email alert failed: {e}")
            return False
    
    def _send_sms_alert(self, message, alert_data):
        """Send SMS alert to recipients"""
        try:
            for recipient in self.alert_recipients:
                if not recipient.get('phone') or not self.twilio_configured:
                    continue
                
                sms_body = f"""
                Microplastics Alert: {message['summary']}
                Location: {alert_data['location']}
                Priority: {self._get_priority(alert_data['type'])}
                Details: {alert_data['details'][:100]}...
                View: https://microplasticsinsight.org
                """
                
                message = self.twilio_client.messages.create(
                    body=sms_body.strip(),
                    from_=os.getenv('TWILIO_PHONE_NUMBER'),
                    to=recipient['phone']
                )
                
                print(f"✅ SMS alert sent to {recipient['name']} ({recipient['phone']}) - SID: {message.sid}")
            
            return True
            
        except Exception as e:
            print(f"❌ SMS alert failed: {e}")
            return False
    
    def _get_priority(self, alert_type):
        """Get alert priority level"""
        priority_map = {
            'hotspot': 'HIGH',
            'threshold': 'MEDIUM', 
            'trend': 'MEDIUM',
            'new_upload': 'LOW'
        }
        return priority_map.get(alert_type, 'LOW')
    
    def _log_alert(self, alert_data, success):
        """Log alert to file"""
        try:
            log_entry = {
                **alert_data,
                'success': success,
                'timestamp': datetime.now().isoformat(),
                'method': 'email' if self.email_configured else 'sms' if self.twilio_configured else 'none'
            }
            
            # Append to log file
            log_file = 'alerts_log.jsonl'
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
        except Exception as e:
            print(f"⚠️ Alert logging failed: {e}")
    
    def check_threshold_alert(self, data, region):
        """Check if current data exceeds alert thresholds"""
        if len(data) == 0:
            return None
        
        avg_conc = data['concentration'].mean()
        max_conc = data['concentration'].max()
        
        if avg_conc > self.thresholds['concentration']:
            return self.send_alert(
                alert_type='threshold',
                location=f"{region} (avg: {avg_conc:.1f})",
                concentration=avg_conc,
                region=region,
                details=f"Regional average exceeds threshold by {avg_conc - self.thresholds['concentration']:.1f} particles/m³"
            )
        elif max_conc > self.thresholds['concentration'] * 2:
            return self.send_alert(
                alert_type='hotspot', 
                location=f"{region} (peak: {max_conc:.1f})",
                concentration=max_conc,
                region=region,
                details="Critical peak concentration detected"
            )
        
        return False
    
    def add_recipient(self, name, email=None, phone=None, role='general'):
        """Add new alert recipient"""
        recipient = {
            'name': name,
            'email': email,
            'phone': phone,
            'role': role,
            'active': True,
            'added': datetime.now().isoformat()
        }
        
        self.alert_recipients.append(recipient)
        self.save_recipients()
        print(f"✅ Added recipient: {name}")
        return recipient

# Global alert manager instance
alert_manager = AlertManager()

def send_alert(location, concentration, region='Unknown', alert_type='threshold', details=''):
    """Convenience function to send alerts"""
    return alert_manager.send_alert(alert_type, location, concentration, region, details)

def check_data_thresholds(data, region):
    """Check if dataset triggers any alerts"""
    return alert_manager.check_threshold_alert(data, region)

# Example usage and testing
if __name__ == "__main__":
    # Test alert system
    print("Testing Alert System...")
    
    # Test threshold alert
    test_data = pd.DataFrame({
        'concentration': [120, 95, 150, 80, 200],
        'region': ['Test Region'] * 5
    })
    
    alert_triggered = check_data_thresholds(test_data, "Test Region")
    print(f"Threshold alert test: {'✅ Triggered' if alert_triggered else 'ℹ️ No alert'}")
    
    # Test adding recipient
    alert_manager.add_recipient("Test User", "test@example.com", "+1234567890", "tester")
    
    print("\nAlert system ready for use!")