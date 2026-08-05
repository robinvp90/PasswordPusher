# frozen_string_literal: true

require "test_helper"

class TenantIsolationTest < ActiveSupport::TestCase
  test "tenant boundaries are isolated by tenant id" do
    tenant_a = TenantBoundary.new("tenant-a")
    tenant_b = TenantBoundary.new("tenant-b")

    assert_equal "tenant-a", tenant_a.tenant_id
    assert_equal "tenant-b", tenant_b.tenant_id
    assert_not_same tenant_a, tenant_b
  end

  test "cross-tenant access is blocked by policy" do
    tenant_a = TenantBoundary.new("tenant-a")
    tenant_b = TenantBoundary.new("tenant-b")

    assert_raises(TenantAccessError) do
      tenant_a.authorize_access!(tenant_b)
    end
  end
end
