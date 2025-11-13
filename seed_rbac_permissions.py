#!/usr/bin/env python3
"""
Seed RBAC Permissions and Roles
Run this script to initialize roles and permissions in the database
"""

from app import app, db, Role, Permission, role_permission

PERMISSIONS = {
    "admin": ["*"],  # Admin has all permissions
    "salesman": ["bills.create", "bills.update", "bills.view", "credits.create", "vendors.view"],
    "computer_organiser": ["vendors.update", "vendors.view", "vendors.create", "ocr.verify", "reports.export", "bills.verify", "bills.view"],
    "delivery_man": ["deliveries.update_status", "deliveries.view"]
}

PERMISSION_DESCRIPTIONS = {
    "*": "All permissions",
    "bills.create": "Create new bills",
    "bills.update": "Update existing bills",
    "bills.view": "View bills",
    "bills.verify": "Verify OCR bills",
    "bills.delete": "Delete bills",
    "credits.create": "Create credit transactions",
    "credits.update": "Update credit transactions",
    "credits.view": "View credits",
    "credits.override_status": "Override credit status",
    "vendors.create": "Create vendors",
    "vendors.update": "Update vendors",
    "vendors.view": "View vendors",
    "vendors.delete": "Delete vendors",
    "ocr.verify": "Verify OCR extracted data",
    "reports.export": "Export reports",
    "deliveries.update_status": "Update delivery status",
    "deliveries.view": "View deliveries",
    "users.create": "Create users",
    "users.update": "Update users",
    "users.delete": "Delete users",
    "users.view": "View users"
}

def seed_rbac():
    with app.app_context():
        try:
            print("Seeding RBAC Permissions and Roles...")
            print("=" * 60)
            
            # Create all permissions
            permission_map = {}
            for code, description in PERMISSION_DESCRIPTIONS.items():
                perm = Permission.query.filter_by(code=code).first()
                if not perm:
                    module = code.split('.')[0] if '.' in code else 'general'
                    perm = Permission(
                        code=code,
                        description=description,
                        module=module
                    )
                    db.session.add(perm)
                    print(f"✅ Created permission: {code}")
                permission_map[code] = perm
            
            db.session.commit()
            
            # Create roles and assign permissions
            for role_name, permission_codes in PERMISSIONS.items():
                # Find or create role
                role = Role.query.filter_by(name=role_name).first()
                if not role:
                    display_name = role_name.replace('_', ' ').title()
                    role = Role(
                        name=role_name,
                        display_name=display_name,
                        description=f"{display_name} role"
                    )
                    db.session.add(role)
                    db.session.flush()
                    print(f"\n✅ Created role: {role_name}")
                
                # Assign permissions
                if permission_codes == ["*"]:
                    # Admin gets all permissions
                    for perm in permission_map.values():
                        if perm not in role.permissions.all():
                            role.permissions.append(perm)
                    print(f"   Assigned all permissions to {role_name}")
                else:
                    for perm_code in permission_codes:
                        if perm_code in permission_map:
                            perm = permission_map[perm_code]
                            if perm not in role.permissions.all():
                                role.permissions.append(perm)
                                print(f"   Assigned: {perm_code}")
            
            db.session.commit()
            print("\n" + "=" * 60)
            print("✅ RBAC seeding completed successfully!")
            print("\nRoles and permissions:")
            for role in Role.query.all():
                perms = [p.code for p in role.permissions.all()]
                print(f"  {role.name}: {len(perms)} permissions")
                if len(perms) <= 10:
                    print(f"    {', '.join(perms)}")
                else:
                    print(f"    {', '.join(perms[:10])}... and {len(perms) - 10} more")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    seed_rbac()

