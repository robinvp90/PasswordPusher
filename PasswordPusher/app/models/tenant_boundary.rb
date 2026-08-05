# frozen_string_literal: true

class TenantBoundary
  attr_reader :tenant_id

  def initialize(tenant_id)
    @tenant_id = tenant_id
  end

  def authorize_access!(target)
    return true if target.respond_to?(:tenant_id) && target.tenant_id == tenant_id

    raise TenantAccessError, "Tenant #{tenant_id} cannot access tenant #{target.respond_to?(:tenant_id) ? target.tenant_id : 'unknown'}"
  end
end
